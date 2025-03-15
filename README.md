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

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

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
└── .github/            # GitHub Actions workflows
```

## License

MIT 