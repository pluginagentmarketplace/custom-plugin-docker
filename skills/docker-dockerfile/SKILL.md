---
name: docker-dockerfile
description: Master Dockerfile - instructions, multi-stage builds, optimization, and best practices
sasmp_version: "1.3.0"
bonded_agent: docker-images
bond_type: PRIMARY_BOND
---

# Docker Dockerfile Skill

## Core Instructions

```dockerfile
FROM node:20-alpine       # Base image
WORKDIR /app              # Set directory
COPY . .                  # Copy files
RUN npm install           # Execute command
ENV NODE_ENV=production   # Set environment
EXPOSE 3000               # Document port
CMD ["node", "app.js"]    # Default command
```

## Multi-Stage Build

```dockerfile
# Build stage
FROM node:20 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/app.js"]
```

## Optimization Tips

1. Order instructions by change frequency
2. Combine RUN commands
3. Use .dockerignore
4. Leverage build cache

## Assets
- `Dockerfile.examples/` - Language templates

## References
- `DOCKERFILE_GUIDE.md` - Best practices
