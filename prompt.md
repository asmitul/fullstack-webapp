I want to build a fully containerized task management web application step by step, and I need your guidance throughout the process. I’m familiar with Python and JavaScript but new to Docker and CI/CD.

Technology Stack:
1.Backend: FastAPI (Python)
2.Frontend: Next.js (React, TypeScript, Tailwind CSS)
3.Database: MongoDB
4.Caching & Message Queue: Redis
5.Reverse Proxy: Nginx
6.Containerization: Docker & Docker Compose
7.CI/CD: GitHub Actions (deploy to a VPS)


Requirements:
1.Set up a development environment with all services running in Docker containers.
2.Build a FastAPI backend with JWT authentication, CRUD APIs for tasks (create, read, update, delete), and basic task management logic.
3.Develop a Next.js frontend with user login, task listing, and task creation UI.
4.Use MongoDB for persistent task storage and Redis for caching task data.
5.Configure Nginx as a reverse proxy for frontend-backend communication.
6.Create a Docker Compose setup to orchestrate all services.
7.Implement CI/CD with GitHub Actions for automated testing and VPS deployment.

Apply performance (e.g., caching) and security (e.g., HTTPS, input validation) best practices.

Please guide me step-by-step, starting with the development environment and project structure. Provide clear explanations, Docker configurations, and minimal working examples (e.g., basic CRUD endpoints and a simple UI) at each stage.