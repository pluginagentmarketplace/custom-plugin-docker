# Multi-Stage Build Patterns

## Pattern 1: Build and Production

The most common pattern - build in one stage, run in another.

```dockerfile
# Build stage
FROM node:20 AS builder
WORKDIR /app
COPY . .
RUN npm ci && npm run build

# Production stage
FROM node:20-alpine
COPY --from=builder /app/dist ./dist
CMD ["node", "dist/index.js"]
```

## Pattern 2: Dependency Caching

Separate dependency installation for better caching.

```dockerfile
# Dependencies stage
FROM node:20-alpine AS deps
COPY package*.json ./
RUN npm ci

# Build stage
FROM node:20-alpine AS builder
COPY --from=deps /node_modules ./node_modules
COPY . .
RUN npm run build

# Production
FROM node:20-alpine
COPY --from=builder /dist ./dist
```

## Pattern 3: Testing Stage

Include testing in the build pipeline.

```dockerfile
FROM python:3.12 AS base
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM base AS test
COPY . .
RUN pytest

FROM base AS production
COPY --from=test /app .
```

## Pattern 4: Development and Production

Same Dockerfile for dev and prod.

```dockerfile
FROM node:20-alpine AS base
WORKDIR /app
COPY package*.json ./

FROM base AS development
RUN npm install
CMD ["npm", "run", "dev"]

FROM base AS production
RUN npm ci --only=production
COPY . .
CMD ["npm", "start"]
```

Build with: `docker build --target=development -t app:dev .`

## Size Comparison Example

| Stage | Image | Size |
|-------|-------|------|
| Single stage | node:20 | ~1GB |
| Multi-stage | node:20-alpine | ~150MB |
| Distroless | gcr.io/distroless | ~50MB |

## Best Practices

1. **Name your stages** - Use `AS stagename`
2. **Order matters** - Put frequently changing steps last
3. **Copy only what's needed** - Use specific paths
4. **Clean up in same layer** - `RUN apt-get install && rm -rf /var/lib/apt/lists/*`
5. **Use .dockerignore** - Exclude node_modules, .git, etc.
