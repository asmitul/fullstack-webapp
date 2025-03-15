#!/bin/bash

# Exit on error
set -e

echo "Setting up Task Management Web Application..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Build and start the containers
echo "Building and starting containers..."
docker-compose build
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 10

echo "Setup complete! You can access the application at:"
echo "- Frontend: http://localhost:3000"
echo "- Backend API: http://localhost:8000"
echo "- API Documentation: http://localhost:8000/docs"

echo "To stop the application, run: docker-compose down" 