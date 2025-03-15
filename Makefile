.PHONY: setup start stop restart logs backend-logs frontend-logs test clean health-check help

# Default target
help:
	@echo "Task Management Web Application Makefile"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  setup        - Set up the development environment and start all containers"
	@echo "  start        - Start all containers"
	@echo "  stop         - Stop all containers"
	@echo "  restart      - Restart all containers"
	@echo "  logs         - Show logs from all containers"
	@echo "  backend-logs - Show logs from backend container"
	@echo "  frontend-logs - Show logs from frontend container"
	@echo "  test         - Run backend tests"
	@echo "  health-check - Check the health of all services"
	@echo "  clean        - Stop all containers and clean up resources"
	@echo "  help         - Show this help message"
	@echo ""

setup:
	@echo "Setting up Task Management Web Application..."
	docker-compose build
	docker-compose up -d
	@echo "Setup complete! You can access the application at:"
	@echo "- Frontend: http://localhost:3000"
	@echo "- Backend API: http://localhost:8000"
	@echo "- API Documentation: http://localhost:8000/docs"

start:
	@echo "Starting containers..."
	docker-compose up -d
	@echo "Containers started."

stop:
	@echo "Stopping containers..."
	docker-compose down
	@echo "Containers stopped."

restart: stop start

logs:
	docker-compose logs -f

backend-logs:
	docker-compose logs -f backend

frontend-logs:
	docker-compose logs -f frontend

test:
	@echo "Running backend tests..."
	docker-compose exec backend pytest

health-check:
	@echo "Checking application health..."
	./health-check.sh

clean:
	@echo "Cleaning up Task Management Web Application..."
	docker-compose down
	@echo "Cleanup complete!" 