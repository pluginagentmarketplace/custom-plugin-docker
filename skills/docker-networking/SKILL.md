---
name: docker-networking
description: Master Docker networking, volumes, and persistent data. Learn bridge networks, custom networks, volume management, and container communication. Use when managing Docker networks or storage.
---

# Docker Networking & Storage

Connect and persist container data.

## Custom Network

```bash
# Create network
docker network create myapp-net

# Run on network
docker run --network myapp-net --name app1 alpine
docker run --network myapp-net --name app2 alpine

# Auto DNS: app1 resolves to app2
```

## Docker Compose Networking

```yaml
services:
  web:
    networks:
      - frontend
      - backend
    environment:
      DB_HOST: postgres  # Auto DNS resolution

  postgres:
    networks:
      - backend

networks:
  frontend:
  backend:
```

## Volumes

```bash
# Named volume
docker volume create mydata
docker run -v mydata:/data myapp

# Bind mount
docker run -v /host/path:/container/path myapp

# Volume inspection
docker volume ls
docker volume inspect mydata
```

## Compose Volumes

```yaml
services:
  db:
    volumes:
      - db_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql

volumes:
  db_data:
    driver: local
```

## Port Mapping

```bash
# Single port
docker run -p 8080:3000 myapp

# Multiple ports
docker run -p 8080:3000 -p 443:443 myapp

# Random port
docker run -P myapp
```

## Key Concepts

- Bridge networks
- Custom networks
- DNS resolution
- Named volumes
- Bind mounts
- Port mapping
- Storage drivers
- Network isolation

## Best Practices

1. Use named volumes (not bind mounts)
2. Create custom networks (isolation)
3. DNS names for service discovery
4. Volume backups for data
5. Read-only mounts when possible
6. Mount options for security
7. Network policies
8. Storage driver choice
