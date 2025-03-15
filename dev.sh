#!/bin/bash

# Exit on error
set -e

function show_help {
    echo "Task Management Web Application Development Script"
    echo ""
    echo "Usage: ./dev.sh [command]"
    echo ""
    echo "Commands:"
    echo "  start       - Start all containers"
    echo "  stop        - Stop all containers"
    echo "  restart     - Restart all containers"
    echo "  logs        - Show logs from all containers"
    echo "  backend     - Show logs from backend container"
    echo "  frontend    - Show logs from frontend container"
    echo "  test        - Run backend tests"
    echo "  health      - Check the health of all services"
    echo "  help        - Show this help message"
    echo ""
}

case "$1" in
    start)
        echo "Starting containers..."
        docker-compose up -d
        echo "Containers started. Access the application at:"
        echo "- Frontend: http://localhost:3000"
        echo "- Backend API: http://localhost:8000"
        echo "- API Documentation: http://localhost:8000/docs"
        ;;
    stop)
        echo "Stopping containers..."
        docker-compose down
        echo "Containers stopped."
        ;;
    restart)
        echo "Restarting containers..."
        docker-compose down
        docker-compose up -d
        echo "Containers restarted."
        ;;
    logs)
        echo "Showing logs from all containers..."
        docker-compose logs -f
        ;;
    backend)
        echo "Showing logs from backend container..."
        docker-compose logs -f backend
        ;;
    frontend)
        echo "Showing logs from frontend container..."
        docker-compose logs -f frontend
        ;;
    test)
        echo "Running backend tests..."
        docker-compose exec backend pytest
        ;;
    health)
        echo "Checking application health..."
        ./health-check.sh
        ;;
    help|*)
        show_help
        ;;
esac 