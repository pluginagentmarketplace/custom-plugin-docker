---
name: docker-containers
description: Master Docker containers - running, managing, debugging, and lifecycle operations
sasmp_version: "1.3.0"
bonded_agent: docker-containers
bond_type: PRIMARY_BOND
---

# Docker Containers Skill

## Running Containers

```bash
# Basic run
docker run nginx

# Detached with name
docker run -d --name web nginx

# Interactive
docker run -it ubuntu bash

# With port mapping
docker run -d -p 8080:80 nginx

# With environment variables
docker run -d -e DB_HOST=localhost myapp

# With resource limits
docker run -d --memory=512m --cpus=1 myapp
```

## Container Management

```bash
# List containers
docker ps          # Running
docker ps -a       # All

# Stop/start
docker stop web
docker start web
docker restart web

# Remove
docker rm web
docker rm -f web   # Force
```

## Debugging

```bash
# Logs
docker logs web
docker logs -f web  # Follow

# Execute command
docker exec -it web bash
docker exec web cat /etc/hosts

# Inspect
docker inspect web
docker stats web
```

## Assets
- `run-examples.sh` - Common patterns

## References
- `CONTAINER_GUIDE.md` - Best practices
