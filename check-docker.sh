#!/bin/bash

# Quick script to check Docker status

echo "Checking Docker installation..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed or not in PATH"
    echo "Please install Docker Desktop from https://www.docker.com/products/docker-desktop/"
    exit 1
fi

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo "❌ Docker daemon is not running"
    echo ""
    echo "Please start Docker Desktop:"
    echo "  - Windows: Launch Docker Desktop from Start Menu"
    echo "  - macOS: Launch Docker Desktop from Applications"
    echo "  - Linux: sudo systemctl start docker"
    exit 1
fi

echo "✅ Docker is installed and running"
echo ""
echo "Docker version:"
docker --version
echo ""
echo "Docker Compose version:"
docker-compose --version
echo ""
echo "You can now run: docker-compose up --build"

