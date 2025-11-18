---
description: Master Docker Compose for multi-container applications. Learn service definition, networking, volumes, environment variables, and scaling containers together.
capabilities: ["Compose file syntax", "Service orchestration", "Volume management", "Environment configuration", "Networking", "Dependencies", "Health checks", "Service scaling", "Production compose patterns"]
---

# 🐳 Docker Compose & Multi-Container Orchestration

## Overview
Production-ready Docker Compose for managing multiple containers as a single application.

## Docker Compose Essentials

### Basic docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    image: node:18-alpine
    build: .
    container_name: app-web
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://db:5432/appdb
    volumes:
      - ./src:/app/src
      - /app/node_modules
    depends_on:
      - db
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:15-alpine
    container_name: app-db
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    networks:
      - app-network

  cache:
    image: redis:7-alpine
    container_name: app-cache
    ports:
      - "6379:6379"
    networks:
      - app-network

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
```

## Essential Commands

```bash
# Startup
docker compose up -d                    # Start services
docker compose up --build               # Rebuild images
docker compose up -d --scale web=3      # Scale service

# Management
docker compose ps                       # List services
docker compose logs -f web              # Follow logs
docker compose exec web bash            # Execute in service
docker compose restart web              # Restart service

# Cleanup
docker compose down                     # Stop and remove
docker compose down -v                  # Remove volumes too
```

## Networking & Communication

```yaml
services:
  web:
    networks:
      - frontend
      - backend

  api:
    networks:
      - backend
    environment:
      - DB_HOST=postgres
      - REDIS_HOST=cache

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
```

## Environment & Secrets

```yaml
# .env file
DB_PASSWORD=secure123
API_KEY=secret456
NODE_ENV=production

# docker-compose.yml
services:
  app:
    environment:
      - DB_PASSWORD=${DB_PASSWORD}
      - API_KEY=${API_KEY}
```

## Learning Path

### Beginner (15 hours)
1. Compose file basics
2. Service definition
3. Port mapping
4. Environment variables
5. Basic networking

### Intermediate (20 hours)
1. Volume management
2. Service dependencies
3. Health checks
4. Scaling services
5. Networking deep dive

### Advanced (15 hours)
1. Production patterns
2. Secret management
3. Resource limits
4. Logging strategies
5. Monitoring setup

## Best Practices

1. **Use explicit image versions** (not latest)
2. **Define health checks** (always)
3. **Set resource limits** (CPU, memory)
4. **Use .env files** (never hardcode secrets)
5. **Define networks explicitly** (container naming)
6. **Volume data persistence** (database volumes)
7. **Depend_on ordering** (doesn't guarantee readiness)
8. **Override for development** (docker-compose.override.yml)
