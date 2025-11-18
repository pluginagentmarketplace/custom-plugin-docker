# /docker-build-run - Docker Build & Run Commands

Essential Docker build and container run commands.

## Description

Quick reference for building Docker images and running containers with best practices.

## Build Commands

```bash
# Basic build
docker build -t myapp:1.0 .

# With build args
docker build --build-arg NODE_ENV=prod -t myapp:1.0 .

# Multi-stage build
docker build --target production -t myapp:1.0 .

# With BuildKit
DOCKER_BUILDKIT=1 docker build -t myapp:1.0 .

# Build and push
docker buildx build --push -t registry.io/myapp:1.0 .
```

## Run Commands

```bash
# Basic run
docker run myapp:1.0

# Detached mode
docker run -d --name myapp myapp:1.0

# Port mapping
docker run -d -p 8080:3000 myapp:1.0

# Environment variables
docker run -d -e NODE_ENV=production myapp:1.0

# Volumes
docker run -d -v mydata:/app/data myapp:1.0

# Resource limits
docker run -d --memory=512m --cpus=0.5 myapp:1.0

# Restart policy
docker run -d --restart=always myapp:1.0

# Full example
docker run -d \
  --name myapp \
  -p 3000:3000 \
  -e NODE_ENV=production \
  -v app_data:/app/data \
  --memory=512m \
  --restart=always \
  myapp:1.0
```

## Best Practices

1. **Always tag images** - Specific versions, not latest
2. **Set restart policy** - `--restart=always`
3. **Resource limits** - `--memory` and `--cpus`
4. **Named containers** - `--name` for easy reference
5. **Health checks** - Include in Dockerfile
6. **Non-root user** - Security first
7. **Logging** - Check `docker logs`
8. **Network** - Custom networks for isolation

## Quick Reference

| Flag | Usage |
|------|-------|
| `-d` | Detached mode |
| `-p` | Port mapping |
| `-e` | Environment variable |
| `-v` | Volume mount |
| `--name` | Container name |
| `--memory` | Memory limit |
| `--cpus` | CPU limit |
| `-i` | Interactive |
| `-t` | Allocate TTY |

## Tips

- Use `docker exec` to enter running containers
- View logs with `docker logs -f container-id`
- Clean up with `docker system prune`
- Use `.dockerignore` to reduce build context
