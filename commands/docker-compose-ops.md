# /docker-compose-ops - Docker Compose Operations

Essential Docker Compose commands for multi-container management.

## Description

Complete reference for managing Docker Compose applications.

## Common Operations

```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# View status
docker compose ps

# View logs
docker compose logs -f
docker compose logs -f app

# Execute command
docker compose exec app bash
docker compose exec app npm test

# Restart service
docker compose restart app
docker compose restart

# Rebuild images
docker compose up -d --build

# Scale service
docker compose up -d --scale web=3
```

## Development Workflow

```bash
# Initial setup
docker compose up -d

# Monitor logs
docker compose logs -f

# Development (watch mode)
docker compose up -d
docker compose exec app npm run dev

# Run migrations
docker compose exec app npm run migrate

# Run tests
docker compose exec app npm test

# Cleanup
docker compose down -v
```

## Production Deployment

```bash
# Pull latest images
docker compose pull

# Build and start
docker compose up -d --build

# Update single service
docker compose up -d --no-deps --build app

# Health check
docker compose ps

# View resource usage
docker compose stats
```

## Docker Compose File Structure

```yaml
version: '3.8'

services:
  # Web service
  app:
    build: .
    ports:
      - "3000:3000"
    depends_on:
      - db
    environment:
      DATABASE_URL: postgres://user:pass@db:5432/appdb

  # Database service
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

## Troubleshooting

```bash
# Check service health
docker compose ps

# View container logs
docker compose logs app

# Inspect service
docker compose exec app bash

# Check network
docker compose exec app ping db

# Resource usage
docker compose stats

# Validate compose file
docker compose config

# Remove stopped containers
docker compose rm
```

## Environment Variables

```bash
# Use .env file
DB_PASSWORD=secret
NODE_ENV=production

# Reference in docker-compose.yml
environment:
  - DATABASE_PASSWORD=${DB_PASSWORD}
```

## Useful Patterns

**Development Override:**
```yaml
# docker-compose.override.yml
services:
  app:
    ports:
      - "3000:3000"
    volumes:
      - ./src:/app/src
```

**Database Initialization:**
```yaml
db:
  image: postgres:15
  volumes:
    - ./init.sql:/docker-entrypoint-initdb.d/init.sql
```

**Health Checks:**
```yaml
services:
  app:
    healthcheck:
      test: curl -f http://localhost:3000/health
      interval: 30s
      timeout: 10s
      retries: 3
```
