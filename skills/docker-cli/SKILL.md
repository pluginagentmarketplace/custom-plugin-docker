---
name: docker-cli
description: Master Docker CLI - essential commands, flags, and productivity tips
sasmp_version: "1.3.0"
bonded_agent: docker-fundamentals
bond_type: SECONDARY_BOND
---

# Docker CLI Skill

## Essential Commands

```bash
# Images
docker images
docker pull nginx
docker build -t myapp .
docker push myapp
docker rmi myapp

# Containers
docker run -d -p 80:80 nginx
docker ps -a
docker stop/start/restart NAME
docker rm NAME
docker logs -f NAME
docker exec -it NAME bash

# System
docker system df
docker system prune -a
docker info
docker version
```

## Useful Flags

```bash
-d          # Detached
-it         # Interactive TTY
-p 8080:80  # Port map
-v /h:/c    # Volume
-e VAR=val  # Environment
--rm        # Remove on exit
--name      # Container name
```

## Assets
- `docker-aliases.sh` - Productivity aliases

## References
- `CLI_GUIDE.md` - Command reference
