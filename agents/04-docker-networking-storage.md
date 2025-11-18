---
description: Master Docker networking, volumes, storage drivers, and container communication. Learn bridge networks, custom networks, volume management, and persistent data strategies.
capabilities: ["Network types", "Custom networks", "DNS resolution", "Port mapping", "Volume management", "Storage drivers", "Data persistence", "Container communication", "Network security"]
---

# 🐳 Docker Networking & Storage

## Overview
Professional Docker networking and persistent data management.

## Network Types

```bash
# Bridge (default)
docker network create --driver bridge mynetwork
docker run --network mynetwork myapp

# Host
docker run --network host myapp

# Custom Bridge
docker network create --subnet=172.20.0.0/16 custom-net
docker run --network custom-net --ip=172.20.0.2 myapp

# Overlay (Swarm/Kubernetes)
docker network create --driver overlay my-overlay
```

## Container Communication

```yaml
# docker-compose.yml - automatic DNS
services:
  web:
    image: myapp
    environment:
      - DB_HOST=postgres
      - CACHE_HOST=redis

  postgres:
    image: postgres:15

  redis:
    image: redis:7

# Service names resolve automatically
# web -> contacts postgres at postgres:5432
```

## Volume Management

```bash
# Named volumes
docker volume create myvolume
docker run -v myvolume:/data myapp

# Bind mounts
docker run -v /host/path:/container/path myapp

# Tmpfs (memory)
docker run --tmpfs /tmp:size=1g myapp

# Volume inspection
docker volume inspect myvolume
docker volume ls
docker volume rm myvolume
```

## Docker Compose Volumes

```yaml
services:
  db:
    image: postgres:15
    volumes:
      - db_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    environment:
      POSTGRES_PASSWORD: secret

  app:
    image: myapp
    volumes:
      - ./src:/app/src          # Bind mount
      - /app/node_modules        # Anonymous

volumes:
  db_data:
    driver: local
```

## Storage Drivers

```bash
# Check current driver
docker info | grep -i "storage driver"

# Common drivers
# overlay2 (Linux) - default, best performance
# btrfs - snapshots
# aufs - legacy
# devicemapper - legacy
```

## Network Isolation

```bash
# Create isolated network
docker network create isolated-net

# Only connected containers can communicate
docker run --network isolated-net service1
docker run --network isolated-net service2

# service1 and service2 can communicate
# But not with external containers
```

## Port Mapping

```bash
# Specific port mapping
docker run -p 8080:3000 myapp
# localhost:8080 -> container:3000

# All ports
docker run -P myapp
# Random port assignment

# Multiple ports
docker run -p 8080:3000 -p 443:443 -p 5432:5432 myapp

# Inspect port mapping
docker port myapp
```

## Data Backup & Restore

```bash
# Backup volume
docker run --rm -v myvolume:/data -v $(pwd):/backup \
  alpine tar czf /backup/backup.tar.gz /data

# Restore volume
docker run --rm -v myvolume:/data -v $(pwd):/backup \
  alpine tar xzf /backup/backup.tar.gz -C /
```

## Learning Path

### Beginner (12 hours)
1. Network basics
2. Port mapping
3. Simple volumes
4. Compose networking
5. Container communication

### Intermediate (18 hours)
1. Custom networks
2. DNS resolution
3. Volume drivers
4. Storage strategies
5. Network policies

### Advanced (15 hours)
1. Advanced networking
2. Multi-host networking
3. Network security
4. Persistent data strategies
5. Backup and recovery

## Best Practices

1. **Use named volumes** (not bind mounts in production)
2. **Create custom networks** (isolation)
3. **Explicit port mapping** (security)
4. **Volume backups** (data safety)
5. **Storage driver choice** (performance)
6. **Network policies** (security)
7. **DNS names** (service discovery)
8. **Mount options** (read-only when possible)
