# Dockerfile Best Practices

## Layer Optimization
- Combine RUN commands with &&
- Put frequently changing commands last
- Use .dockerignore

## Security
- Use non-root USER
- Scan for vulnerabilities
- Pin versions

## Performance
- Use multi-stage builds
- Leverage build cache
- Use alpine/slim images
