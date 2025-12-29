# Docker Security Guide

## Security Checklist

- [ ] Use minimal base images
- [ ] Run as non-root user
- [ ] Scan for vulnerabilities
- [ ] Use read-only filesystem
- [ ] Drop all capabilities
- [ ] Enable no-new-privileges
- [ ] Use secrets management
- [ ] Pin image versions

## Dockerfile Security

```dockerfile
FROM alpine:3.19
RUN adduser -D -u 1001 appuser
USER appuser
```

## Runtime Flags

```bash
docker run \
  --read-only \
  --user 1001 \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  myapp
```
