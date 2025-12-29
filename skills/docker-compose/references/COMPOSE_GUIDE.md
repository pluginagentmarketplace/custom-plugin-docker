# Docker Compose Guide

## depends_on Conditions

```yaml
depends_on:
  db:
    condition: service_healthy
```

## Override Files

```bash
# Base + override
docker compose -f docker-compose.yml -f docker-compose.prod.yml up
```

## Best Practices

1. Use health checks
2. Define explicit networks
3. Use env files for secrets
4. Pin image versions
