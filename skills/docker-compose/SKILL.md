---
name: docker-compose
description: Master Docker Compose - multi-container apps, service orchestration, development workflows
sasmp_version: "1.3.0"
bonded_agent: docker-compose
bond_type: PRIMARY_BOND
---

# Docker Compose Skill

## Basic Structure

```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
  api:
    build: ./api
    environment:
      - DB_HOST=db
  db:
    image: postgres:15
    volumes:
      - db-data:/var/lib/postgresql/data
volumes:
  db-data:
```

## Commands

```bash
docker compose up -d
docker compose down
docker compose ps
docker compose logs -f
docker compose build
docker compose exec api bash
```

## Development Setup

```yaml
services:
  app:
    build: .
    volumes:
      - .:/app          # Hot reload
      - /app/node_modules
    command: npm run dev
```

## Assets
- `docker-compose.yml` - Full stack template

## References
- `COMPOSE_GUIDE.md` - Best practices
