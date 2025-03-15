#!/bin/bash

# Exit on error
set -e

echo "Performing health check for Task Management Web Application..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if containers are running
if ! docker-compose ps | grep -q "Up"; then
    echo "❌ Containers are not running. Please start the application first."
    echo "Run: ./setup.sh or docker-compose up -d"
    exit 1
fi

# Check backend health
echo "Checking backend health..."
if docker-compose exec -T backend python health.py; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend is not responding properly"
    echo "Check logs: docker-compose logs backend"
fi

# Check frontend health
echo "Checking frontend health..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200"; then
    echo "✅ Frontend is healthy"
else
    echo "❌ Frontend is not responding properly"
    echo "Check logs: docker-compose logs frontend"
fi

# Check MongoDB connection
echo "Checking MongoDB connection..."
if docker-compose exec -T mongodb mongosh --eval "db.runCommand({ping: 1})" | grep -q "ok: 1"; then
    echo "✅ MongoDB is connected"
else
    echo "❌ MongoDB connection issue"
    echo "Check logs: docker-compose logs mongodb"
fi

# Check Redis connection
echo "Checking Redis connection..."
if docker-compose exec -T redis redis-cli ping | grep -q "PONG"; then
    echo "✅ Redis is connected"
else
    echo "❌ Redis connection issue"
    echo "Check logs: docker-compose logs redis"
fi

echo "Health check completed." 