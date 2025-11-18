---
name: docker-basics
description: Docker fundamentals including images, containers, Dockerfile syntax, and Docker CLI. Learn containerization, layer concepts, and basic container lifecycle. Use when working with Docker containers or images.
---

# Docker Basics

Master Docker fundamentals and containerization.

## Quick Start

```bash
# Pull and run
docker pull alpine:3.18
docker run -it alpine:3.18 sh

# Build image
docker build -t myapp:1.0 .
docker run -p 3000:3000 myapp:1.0

# View info
docker ps -a
docker images
docker logs container-id
```

## Essential Dockerfile

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY src ./src
EXPOSE 3000
CMD ["node", "src/index.js"]
```

## Core Commands

- `docker build` - Build images
- `docker run` - Run containers
- `docker ps` - List containers
- `docker logs` - View container logs
- `docker exec` - Execute commands in container
- `docker images` - List images
- `docker pull/push` - Registry operations
- `docker compose` - Multi-container orchestration

## Image Layers

```dockerfile
# Each line creates a layer
FROM alpine        # Layer 1
RUN apk add curl   # Layer 2
COPY app .         # Layer 3
CMD ["./app"]      # Layer 4
```

## Best Practices

1. Use specific base image versions (not `latest`)
2. Combine RUN commands (reduce layers)
3. Order commands from stable to volatile (caching)
4. Use .dockerignore (smaller context)
5. Run as non-root user (security)
6. Keep images small (alpine base)
