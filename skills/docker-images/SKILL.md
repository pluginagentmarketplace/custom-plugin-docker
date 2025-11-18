---
name: docker-images
description: Master Docker image building, optimization, and registry management. Learn multi-stage builds, layer caching, and pushing to registries. Use when building or managing Docker images.
---

# Docker Images

Build and optimize production images.

## Multi-Stage Build

```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /build
COPY package*.json ./
RUN npm ci

# Runtime stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /build/node_modules ./node_modules
COPY src ./src
CMD ["node", "src/index.js"]
```

## Image Optimization

```dockerfile
# Single layer approach
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Layer caching - order matters
FROM alpine
COPY package.json .          # Stable, changes less
RUN npm install              # Cached if package.json unchanged
COPY src .                   # Volatile, changes often
```

## Registry Commands

```bash
# Tag image
docker tag myapp:1.0 registry.io/myapp:1.0

# Push
docker login registry.io
docker push registry.io/myapp:1.0

# Pull
docker pull registry.io/myapp:1.0

# Inspect
docker image inspect myapp:1.0
docker history myapp:1.0
```

## Build Arguments

```dockerfile
ARG NODE_ENV=production
ENV NODE_ENV=${NODE_ENV}

FROM node:18-alpine
RUN npm install --production
```

```bash
docker build --build-arg NODE_ENV=development -t myapp:dev .
```

## Key Concepts

- Image layers
- Layer caching
- Build context
- .dockerignore
- Build args
- Multi-stage builds
- Image tagging
- Registry management

## Best Practices

1. Minimize layers
2. Leverage caching
3. Use .dockerignore
4. Specific base versions
5. Non-root users
6. Health checks
7. Proper tagging
8. Image scanning
