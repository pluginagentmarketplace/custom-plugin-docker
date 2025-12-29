---
name: docker-devex
description: Docker developer experience - hot reloading, debugging, testing, and CI integration
sasmp_version: "1.3.0"
bonded_agent: docker-production
bond_type: SECONDARY_BOND
---

# Docker Developer Experience Skill

## Hot Reloading

```yaml
services:
  app:
    build: .
    volumes:
      - .:/app
      - /app/node_modules
    command: npm run dev
```

## Debugging

```yaml
services:
  app:
    ports:
      - "9229:9229"  # Node debugger
    command: node --inspect=0.0.0.0:9229 app.js
```

## Testing

```bash
# Run tests in container
docker compose run --rm app npm test

# CI testing
docker compose -f docker-compose.test.yml up --abort-on-container-exit
```

## Assets
- `docker-compose.dev.yml` - Development setup

## References
- `DEVEX_GUIDE.md` - Workflow tips
