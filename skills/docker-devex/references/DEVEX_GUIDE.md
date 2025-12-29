# Docker Developer Experience Guide

## Hot Reload Setup

1. Mount source code as volume
2. Exclude node_modules
3. Use development command

## Debugging in Container

### Node.js
```bash
node --inspect=0.0.0.0:9229 app.js
```

### Python
```bash
python -m debugpy --listen 0.0.0.0:5678 app.py
```

## Best Practices

1. Use multi-stage builds (dev target)
2. Keep dev and prod configs separate
3. Use .dockerignore
4. Cache dependencies
