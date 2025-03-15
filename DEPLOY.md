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

### Option 1: Generate on your local machine (Recommended)

On your local machine (not the VPS):

```bash
# Generate SSH key pair
ssh-keygen -t ed25519 -C "github-actions-deploy"

# Copy the public key to your VPS
cat ~/.ssh/id_ed25519.pub | ssh deploy@your-vps-ip "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

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

## 4. Prepare the Application Directory

On your VPS, as the deploy user:

```bash
# Switch to the deploy user
su - deploy

# Create application directory
mkdir -p ~/task-management-app
```

## 5. Configure Nginx (Optional, for Domain Setup)

If you have a domain name and want to use it:

```bash
# Install Nginx
sudo apt install -y nginx

# Create Nginx configuration
sudo nano /etc/nginx/sites-available/task-management-app
```

Add the following configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable the configuration:

```bash
sudo ln -s /etc/nginx/sites-available/task-management-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 6. Set Up SSL with Let's Encrypt (Optional)

If you have a domain:

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

## 7. Manual Deployment (If Needed)

If you need to deploy manually without GitHub Actions:

```bash
# Switch to the deploy user
su - deploy

# Clone the repository
cd ~
git clone https://github.com/yourusername/task-management-app.git
cd task-management-app

# Start the application
docker-compose up -d
```

## 8. Verify Deployment

After deployment (either manual or via GitHub Actions), verify that everything is working:

```bash
# Check container status
docker-compose ps

# Run health check
./health-check.sh
```

## 9. Troubleshooting

### Check container logs

```bash
docker-compose logs backend
docker-compose logs frontend
```

### Restart containers

```bash
docker-compose restart
```

### Rebuild containers

```bash
docker-compose down
docker-compose build
docker-compose up -d
```

## 10. Maintenance

### Update the application

GitHub Actions will automatically deploy when you push to the main branch. For manual updates:

```bash
cd ~/task-management-app
git pull
docker-compose down
docker-compose build
docker-compose up -d
```

### Backup the database

```bash
# Create a backup directory
mkdir -p ~/backups

# Backup MongoDB data
docker-compose exec -T mongodb mongodump --archive > ~/backups/mongodb-backup-$(date +%Y%m%d).archive
```

## 11. Security Considerations

- Keep your server updated: `sudo apt update && sudo apt upgrade -y`
- Configure a firewall: `sudo ufw enable && sudo ufw allow ssh && sudo ufw allow http && sudo ufw allow https`
- Set up fail2ban: `sudo apt install -y fail2ban`
- Regularly rotate SSH keys
- Monitor logs for suspicious activity 