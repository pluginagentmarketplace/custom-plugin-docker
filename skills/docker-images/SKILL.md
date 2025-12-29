---
name: docker-images
description: Master Docker images - pulling, building, tagging, pushing, and image layer management
sasmp_version: "1.3.0"
bonded_agent: docker-images
bond_type: PRIMARY_BOND
---

# Docker Images Skill

## Core Commands

```bash
# List images
docker images
docker image ls

# Pull image
docker pull nginx:alpine
docker pull ubuntu:22.04

# Build image
docker build -t myapp:v1 .
docker build -t myapp:v1 -f Dockerfile.prod .

# Tag image
docker tag myapp:v1 registry.com/myapp:v1

# Push image
docker push registry.com/myapp:v1

# Remove image
docker rmi myapp:v1
docker image prune -a
```

## Image Inspection

```bash
# Inspect layers
docker history myapp:v1

# Detailed info
docker inspect myapp:v1

# Image size
docker images --format "{{.Repository}}:{{.Tag}} {{.Size}}"
```

## Assets
- `Dockerfile.template` - Production template

## References
- `IMAGE_GUIDE.md` - Best practices
