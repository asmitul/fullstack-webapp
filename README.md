# Task Management Web Application

A fully containerized task management web application built with modern technologies.

## Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Next.js (React, TypeScript, Tailwind CSS)
- **Database**: MongoDB
- **Caching & Message Queue**: Redis
- **Reverse Proxy**: Nginx
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions

## Features

- User authentication with JWT
- Task management (create, read, update, delete)
- Responsive UI
- Containerized development and production environments
- Automated testing and deployment

## Development Setup

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/task-management-app.git
   cd task-management-app
   ```

2. Start the application with Docker Compose:
   ```bash
   docker-compose up -d
   ```
   
   Or use the setup script:
   ```bash
   ./setup.sh
   ```
   
   Or use Make:
   ```bash
   make setup
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Helper Scripts

The project includes several helper scripts to make development easier:

- **setup.sh**: Sets up the development environment and starts all containers
  ```bash
  ./setup.sh
  ```

- **dev.sh**: Development workflow script with various commands
  ```bash
  ./dev.sh [command]
  ```
  Available commands:
  - `start`: Start all containers
  - `stop`: Stop all containers
  - `restart`: Restart all containers
  - `logs`: Show logs from all containers
  - `backend`: Show logs from backend container
  - `frontend`: Show logs from frontend container
  - `test`: Run backend tests
  - `health`: Check the health of all services
  - `help`: Show help message

- **cleanup.sh**: Stops all containers and cleans up resources
  ```bash
  ./cleanup.sh
  ```

- **health-check.sh**: Checks the health of all services
  ```bash
  ./health-check.sh
  ```

- **Makefile**: Provides Make targets for common operations
  ```bash
  make [target]
  ```
  Available targets:
  - `setup`: Set up the development environment and start all containers
  - `start`: Start all containers
  - `stop`: Stop all containers
  - `restart`: Restart all containers
  - `logs`: Show logs from all containers
  - `backend-logs`: Show logs from backend container
  - `frontend-logs`: Show logs from frontend container
  - `test`: Run backend tests
  - `health-check`: Check the health of all services
  - `clean`: Stop all containers and clean up resources
  - `help`: Show help message

### Development Workflow

#### Backend Development

The backend code is in the `backend` directory. It's a FastAPI application with the following structure:

- `app/`: Main application package
  - `api/`: API endpoints
  - `core/`: Core functionality (config, security)
  - `db/`: Database connections
  - `models/`: Data models
  - `schemas/`: Pydantic schemas
  - `services/`: Business logic
  - `utils/`: Utility functions
- `tests/`: Test files
- `main.py`: Application entry point

To run the backend tests:

```bash
docker-compose exec backend pytest
```

Or use the dev script:

```bash
./dev.sh test
```

Or use Make:

```bash
make test
```

#### Frontend Development

The frontend code is in the `frontend` directory. It's a Next.js application with the following structure:

- `app/`: Next.js app directory
- `components/`: React components
- `lib/`: Utility functions and API clients
- `public/`: Static files

To run the frontend tests:

```bash
docker-compose exec frontend npm run test
```

## API Documentation

The API documentation is available at http://localhost:8000/docs when the application is running.

## Deployment

The application can be deployed to a VPS using GitHub Actions. The workflow is defined in `.github/workflows/deploy.yml`.

For detailed deployment instructions, please refer to the [Deployment Guide](DEPLOY.md).

To set up deployment, you need to add the following secrets to your GitHub repository:

- `SSH_PRIVATE_KEY`: SSH private key for accessing the VPS
- `VPS_HOST`: Hostname or IP address of the VPS
- `VPS_USER`: Username for SSH access
- `VPS_PATH`: Path to the application directory on the VPS

## Project Structure

```
.
├── backend/            # FastAPI backend
├── frontend/           # Next.js frontend
├── nginx/              # Nginx configuration
├── mongodb/            # MongoDB data and configuration
├── redis/              # Redis data and configuration
├── docker-compose.yml  # Docker Compose configuration
├── .github/            # GitHub Actions workflows
├── setup.sh            # Setup script
├── dev.sh              # Development workflow script
├── cleanup.sh          # Cleanup script
├── health-check.sh     # Health check script
└── Makefile            # Make targets for common operations
```

## Troubleshooting

### Backend API Not Accessible

If the backend API at http://localhost:8000 is not accessible:

1. Check if the backend container is running:
   ```bash
   docker-compose ps
   ```

2. Check the backend logs for errors:
   ```bash
   docker-compose logs backend
   ```

3. Common issues:
   - **Missing email-validator package**: If you see an error about `email_validator` module, install it:
     ```bash
     docker-compose exec backend pip install email-validator
     docker-compose restart backend
     ```
   - **Port conflict**: Make sure no other service is using port 8000
   - **Database connection issues**: Check if MongoDB is running and accessible

### Frontend Issues

If the frontend at http://localhost:3000 has issues:

1. Check if the frontend container is running:
   ```bash
   docker-compose ps
   ```

2. Check the frontend logs for errors:
   ```bash
   docker-compose logs frontend
   ```

3. Common issues:
   - **TypeScript errors**: Make sure all required type definitions are installed
   - **API connection errors**: Verify that the backend API is accessible

### Health Check

Run the health check script to verify all services are running properly:
```bash
./health-check.sh
```

## License

MIT 