---
description: Master Docker image building, optimization, and registry management. Learn multi-stage builds, image layers, caching strategies, and pushing to registries.
capabilities: ["Multi-stage builds", "Image optimization", "Layer analysis", "Cache strategy", "Registry management", "Image tagging", "Image scanning", "Build context", "Dockerfile best practices"]
---

# 🐳 Docker Image Management

## Overview
Professional Docker image building, optimization, and registry operations.

## Multi-Stage Dockerfile

```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /build
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Runtime
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /build/node_modules ./node_modules
COPY src ./src
COPY package.json .
EXPOSE 3000
USER node
CMD ["node", "src/index.js"]
```

## Image Layer Optimization

```dockerfile
# WRONG - Creates multiple layers
RUN apt-get update
RUN apt-get install -y curl wget
RUN apt-get clean

# CORRECT - Single layer
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
```

## Dockerfile Best Practices

```dockerfile
FROM alpine:3.18

# Set labels
LABEL maintainer="team@example.com"
LABEL version="1.0"

# Use build arguments
ARG NODE_ENV=production

# Set working directory
WORKDIR /app

# Copy package files first (caching)
COPY package*.json ./
RUN npm ci --production

# Copy application code
COPY src ./src
COPY public ./public

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001
USER nodejs

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

# Expose port
EXPOSE 3000

# Start command
CMD ["node", "src/index.js"]
```

## Image Management Commands

```bash
# Building
docker build -t myapp:1.0 .
docker build -t myapp:latest -t myapp:1.0 .
docker build --build-arg NODE_ENV=prod -t myapp:1.0 .

# Tagging & Pushing
docker tag myapp:1.0 registry.example.com/myapp:1.0
docker push registry.example.com/myapp:1.0

# Inspection
docker image inspect myapp:1.0
docker image history myapp:1.0
docker image ls --digests

# Cleaning
docker image prune -a
docker image rm myapp:1.0
```

## Registry Operations

```bash
# Docker Hub
docker login
docker tag myapp:1.0 username/myapp:1.0
docker push username/myapp:1.0

# Private Registry
docker login registry.example.com
docker tag myapp:1.0 registry.example.com/myapp:1.0
docker push registry.example.com/myapp:1.0

# Image Scanning
docker scan myapp:1.0
```

## .dockerignore

```
.git
.gitignore
node_modules
npm-debug.log
.env
.env.local
.DS_Store
.vscode
.idea
dist
build
coverage
*.log
```

## Learning Path

### Beginner (15 hours)
1. Dockerfile syntax
2. Image building basics
3. Layer concepts
4. Simple optimization
5. Basic tagging

### Intermediate (20 hours)
1. Multi-stage builds
2. Advanced caching
3. Image inspection
4. Registry basics
5. Environment variables

### Advanced (15 hours)
1. Image scanning security
2. Advanced optimization
3. Build performance
4. Registry management
5. Production patterns

## Best Practices

1. **Start with smallest base image** (alpine, distroless)
2. **One process per container** (follow Unix philosophy)
3. **Minimize layers** (combine commands)
4. **Order matters for caching** (stable to volatile)
5. **Use .dockerignore** (reduce context size)
6. **Non-root user** (security)
7. **Health checks always** (container readiness)
8. **Specific version tags** (reproducibility)
