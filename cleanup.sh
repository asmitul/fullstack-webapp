#!/bin/bash

# Exit on error
set -e

echo "Cleaning up Task Management Web Application..."

# Stop and remove containers
echo "Stopping and removing containers..."
docker-compose down

# Remove volumes (optional, uncomment if needed)
# echo "Removing volumes..."
# docker volume rm $(docker volume ls -q -f name=fullstack-webapp_mongodb-data)
# docker volume rm $(docker volume ls -q -f name=fullstack-webapp_redis-data)

echo "Cleanup complete!" 