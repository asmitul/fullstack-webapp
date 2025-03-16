# Deployment Guide for Task Management Web Application

This guide will walk you through deploying the Task Management Web Application to a Virtual Private Server (VPS).

## Prerequisites

- A VPS with SSH access (Ubuntu 20.04 or newer recommended)
- Domain name (optional, but recommended)
- GitHub account with your repository

## 1. Initial VPS Setup

### SSH into your VPS

```bash
ssh root@your-vps-ip
```

### Update the system

```bash
apt update && apt upgrade -y
```

### Install required software

```bash
# Install Docker and Docker Compose
apt install -y docker.io docker-compose git

# Start and enable Docker
systemctl start docker
systemctl enable docker
```

### Create a non-root user for deployment

```bash
# Create a new user
adduser deploy

# Add user to sudo and docker groups
usermod -aG sudo deploy
usermod -aG docker deploy
```

## 2. Set Up SSH Keys for GitHub Actions

You have two options for generating SSH keys:

### Option 2: Generate on your VPS

On your VPS:

```bash
# Switch to the deploy user
su - deploy

# Generate SSH key pair
ssh-keygen -t ed25519 -C "github-actions-deploy"

# Add the public key to authorized_keys
cat ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# Display the private key (copy this for GitHub)
cat ~/.ssh/id_ed25519

# Remove the private key from the server (for security)
rm ~/.ssh/id_ed25519
```

## 3. Add Secrets to GitHub Repository

1. Go to your GitHub repository
2. Click on "Settings" > "Secrets and variables" > "Actions"
3. Add the following secrets:
   - `SSH_PRIVATE_KEY`: Your private key (entire content including BEGIN and END lines)
   - `VPS_HOST`: Your VPS IP address
   - `VPS_USER`: `deploy` (or whatever username you created)
   - `VPS_PATH`: `/home/deploy/task-management-app`
   - `JWT_SECRET` : 
   - `MONGODB_URI` : `mongodb://mongodb:27017/taskdb`
   - `NEXT_PUBLIC_API_URL` : `http://ip:8000`
   - `REDIS_HOST` : `localhost`
   - `REDIS_PORT` : `6379`

## 4. Prepare the Application Directory

On your VPS, as the deploy user:

```bash
# Switch to the deploy user
su - deploy

# Create application directory
mkdir -p ~/task-management-app
```