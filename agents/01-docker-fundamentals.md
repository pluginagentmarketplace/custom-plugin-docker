---
description: Master Docker fundamentals including images, containers, Dockerfile syntax, and Docker CLI. Learn containerization concepts, image layers, and basic container lifecycle management.
capabilities: ["Dockerfile creation", "Image building", "Container basics", "Docker CLI", "Image layers", "Registry operations", "Container lifecycle", "Port mapping", "Volume mounting"]
---

# 🐳 Docker Fundamentals

## Overview
Complete guide to Docker basics - images, containers, and containerization concepts.

## Core Concepts

### Images vs Containers
- **Image**: Blueprint, immutable, static
- **Container**: Running instance, mutable, dynamic

### Dockerfile Essentials
```dockerfile
FROM alpine:3.18
WORKDIR /app
COPY . .
RUN apk add --no-cache python3
EXPOSE 5000
CMD ["python3", "app.py"]
```

### Docker CLI Essentials
```bash
# Images
docker images                          # List images
docker pull node:18                    # Pull image
docker build -t myapp:1.0 .           # Build image
docker rmi myapp:1.0                  # Remove image

# Containers
docker run -d --name myapp -p 3000:3000 myapp:1.0
docker ps                              # List running
docker stop myapp                      # Stop container
docker rm myapp                        # Remove container
docker logs myapp                      # View logs
docker exec -it myapp bash            # Enter container
```

## Learning Path

### Beginner (20 hours)
1. Container concepts
2. Basic Dockerfile
3. Building and running containers
4. Port mapping basics
5. Volume mounting introduction

### Intermediate (25 hours)
1. Multi-stage builds
2. Image optimization
3. Layer caching
4. Docker compose introduction
5. Container networking basics

### Advanced (20 hours)
1. Registry management
2. Image scanning
3. Performance optimization
4. Production patterns
5. Security hardening

## Best Practices

1. **Use specific base image tags** (not `latest`)
2. **Minimize image layers** (combine RUN commands)
3. **Leverage build cache** (order matters)
4. **Remove unnecessary files** (.dockerignore)
5. **Use HEALTHCHECK** for container health
6. **Set resource limits**
7. **Run as non-root user**

## Key Commands

```bash
docker build -t <name>:<tag> .
docker run -d -p <host>:<container> <image>
docker compose up -d
docker ps -a
docker logs -f <container>
docker exec -it <container> /bin/bash
```
