---
name: docker-compose
description: Master Docker Compose for multi-container applications. Learn service definition, networking, volumes, environment configuration, and scaling. Use when managing multiple containers together.
---

# Docker Compose

Production multi-container orchestration.

## Quick Start

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DB_HOST=postgres
    depends_on:
      - postgres

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

## Common Commands

```bash
docker compose up -d                # Start
docker compose down                 # Stop
docker compose logs -f app          # View logs
docker compose exec app bash        # Execute
docker compose restart              # Restart
```

## Service Configuration

```yaml
services:
  web:
    image: node:18
    build: .
    container_name: app
    ports:
      - "3000:3000"
    environment:
      NODE_ENV: production
    volumes:
      - ./src:/app/src
    depends_on:
      - db
    restart: always
    healthcheck:
      test: curl -f http://localhost:3000
      interval: 30s
```

## Key Features

- Service definition
- Network creation
- Volume management
- Environment variables
- Dependency ordering
- Health checks
- Auto-restart
- Service scaling

## Best Practices

1. Use version 3.8+
2. Explicit image versions
3. Always define health checks
4. Set restart policies
5. Use named volumes for data
6. Define networks explicitly
7. Environment files for secrets
8. Override for local development
