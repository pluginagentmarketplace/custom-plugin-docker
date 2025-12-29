# Docker Containers Guide

## Lifecycle States

```
Created → Running → Paused → Stopped → Removed
```

## Restart Policies

| Policy | Description |
|--------|-------------|
| no | Never restart |
| always | Always restart |
| unless-stopped | Restart unless manually stopped |
| on-failure:N | Restart on failure, max N times |

## Resource Limits

```bash
--memory=512m     # Memory limit
--cpus=1.5        # CPU limit
--memory-swap=1g  # Swap limit
```

## Best Practices

1. Use specific image tags
2. Set resource limits
3. Configure restart policies
4. Use health checks
5. Log to stdout/stderr
