# Docker Images Best Practices

## Base Image Selection

| Use Case | Recommended |
|----------|-------------|
| Node.js | node:20-alpine |
| Python | python:3.12-slim |
| Java | eclipse-temurin:21-jre-alpine |
| Go | scratch or distroless |

## Size Optimization

1. Use multi-stage builds
2. Choose slim/alpine bases
3. Combine RUN commands
4. Use .dockerignore
5. Remove cache in same layer

## Layer Caching

```dockerfile
# Good: Dependencies first
COPY package*.json ./
RUN npm ci
COPY . .

# Bad: Invalidates cache
COPY . .
RUN npm ci
```

## Security

- Don't run as root
- Scan for vulnerabilities
- Use specific tags (not :latest)
- Sign images
