# Docker Setup Guide

## Prerequisites

### Windows
1. **Install Docker Desktop**
   - Download from: https://www.docker.com/products/docker-desktop/
   - Install and restart your computer if prompted
   - Launch Docker Desktop and wait for it to start (whale icon in system tray)

2. **Verify Installation**
   ```bash
   docker --version
   docker-compose --version
   ```

3. **Check Docker Status**
   - Look for Docker Desktop icon in system tray
   - Right-click → "Open Docker Desktop" to see status
   - Ensure it shows "Docker Desktop is running"

### Linux
```bash
# Install Docker
sudo apt-get update
sudo apt-get install docker.io docker-compose

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to docker group (optional, to avoid sudo)
sudo usermod -aG docker $USER
```

### macOS
- Install Docker Desktop from https://www.docker.com/products/docker-desktop/
- Launch Docker Desktop from Applications

## Common Issues

### Windows: "The system cannot find the file specified"

**Problem**: Docker Desktop is not running or not properly installed.

**Solutions**:
1. **Start Docker Desktop**
   - Open Docker Desktop application
   - Wait for it to fully start (whale icon should be steady, not animated)
   - Check system tray for Docker icon

2. **Restart Docker Desktop**
   - Right-click Docker icon in system tray
   - Select "Restart Docker Desktop"
   - Wait for restart to complete

3. **Verify Docker Engine**
   ```bash
   docker ps
   ```
   Should return an empty list or running containers, not an error.

4. **Check WSL 2 (if using)**
   - Docker Desktop on Windows uses WSL 2 backend
   - Ensure WSL 2 is installed and updated
   - In Docker Desktop: Settings → General → "Use the WSL 2 based engine"

### Connection Errors

If you see connection errors like:
```
error during connect: Get "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/v1.47/..."
```

**Solutions**:
1. Restart Docker Desktop completely
2. Check Windows Services:
   - Press `Win + R`, type `services.msc`
   - Look for "Docker Desktop Service"
   - Ensure it's running

3. Reset Docker Desktop:
   - Docker Desktop → Settings → Troubleshoot → "Reset to factory defaults"
   - **Warning**: This will remove all containers and images

## Running the Application

Once Docker Desktop is running:

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Verify Services

After starting, verify services are running:

```bash
# Check running containers
docker-compose ps

# Test Next.js app
curl http://localhost:3000/api/health

# Test Java backend
curl http://localhost:8080/api/v1/events
```

## Alternative: Run Without Docker

If Docker continues to cause issues, you can run services locally:

### Next.js App
```bash
cd nextjs-app
npm install
npm run dev
```

### Java Backend
```bash
cd java-backend
mvn clean install
mvn spring-boot:run
```

Make sure databases are initialized first:
```bash
cd databases
python init_databases.py
```

