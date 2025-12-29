# Docker Networks Guide

## DNS Resolution

Containers on same network resolve by name:
```bash
# From app container
ping db  # Works!
```

## Port Publishing

```bash
-p 8080:80      # Host:Container
-p 80           # Random host port
-P              # All exposed ports
```

## Best Practices

1. Use custom networks
2. Isolate by tier
3. Avoid --link (deprecated)
4. Use DNS names
