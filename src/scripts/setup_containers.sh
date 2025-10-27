#!/bin/bash

echo "Setting up compiler system containers..."

# Build and start containers
docker-compose -f docker/docker-compose.yml up -d --build

echo "Containers started successfully!"
echo "API available at: http://localhost:8000"
echo "Redis available at: localhost:6379"

# Wait for services to be ready
sleep 5

# Test API health
curl -f http://localhost:8000/health || echo "API health check failed"

echo "Setup completed!"