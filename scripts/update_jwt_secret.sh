#!/bin/bash

# Script to update JWT secret to a strong, random value
# This addresses a high-priority security task from the TODO list
# usages: ./scripts/update_jwt_secret.sh

set -e  # Exit on any error

echo "Updating JWT secret to a strong, random value..."

# Generate a secure random JWT secret (64 characters)
NEW_JWT_SECRET=$(openssl rand -base64 48 | tr -d '\n/+=' | cut -c1-64)

echo "Generated new JWT secret."

# Update the JWT secret in the backend config file
CONFIG_FILE="backend/app/core/config.py"
if [ -f "$CONFIG_FILE" ]; then
    # Create a backup of the original file
    cp "$CONFIG_FILE" "${CONFIG_FILE}.bak"
    
    # Replace the JWT secret in the config file
    sed -i '' "s/JWT_SECRET: str = \".*\"/JWT_SECRET: str = \"$NEW_JWT_SECRET\"/" "$CONFIG_FILE"
    echo "Updated JWT secret in $CONFIG_FILE"
else
    echo "Error: Config file $CONFIG_FILE not found!"
    exit 1
fi

# Update the JWT secret in docker-compose.yml
DOCKER_COMPOSE_FILE="docker-compose.yml"
if [ -f "$DOCKER_COMPOSE_FILE" ]; then
    # Create a backup of the original file
    cp "$DOCKER_COMPOSE_FILE" "${DOCKER_COMPOSE_FILE}.bak"
    
    # Replace the JWT secret in docker-compose.yml
    sed -i '' "s/JWT_SECRET=.*/JWT_SECRET=$NEW_JWT_SECRET/" "$DOCKER_COMPOSE_FILE"
    echo "Updated JWT secret in $DOCKER_COMPOSE_FILE"
else
    echo "Error: Docker Compose file $DOCKER_COMPOSE_FILE not found!"
    exit 1
fi

# Create a .env file for local development (if it doesn't exist)
ENV_FILE=".env"
if [ ! -f "$ENV_FILE" ]; then
    echo "JWT_SECRET=$NEW_JWT_SECRET" > "$ENV_FILE"
    echo "Created $ENV_FILE with the new JWT secret"
else
    # Update existing .env file
    if grep -q "JWT_SECRET=" "$ENV_FILE"; then
        sed -i '' "s/JWT_SECRET=.*/JWT_SECRET=$NEW_JWT_SECRET/" "$ENV_FILE"
    else
        echo "JWT_SECRET=$NEW_JWT_SECRET" >> "$ENV_FILE"
    fi
    echo "Updated JWT secret in $ENV_FILE"
fi

echo ""
echo "JWT secret has been successfully updated in all necessary files."
echo "IMPORTANT: You will need to restart your services for the changes to take effect:"
echo "  docker-compose down && docker-compose up -d"
echo ""
echo "✅ Task completed: Update JWT secret to a strong, random value for production" 