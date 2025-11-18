---
name: docker-security
description: Production Docker security and best practices. Learn image hardening, secrets management, network security, monitoring, and compliance. Use when securing Docker for production.
---

# Docker Security & Production

Secure and harden Docker for production.

## Secure Dockerfile

```dockerfile
FROM alpine:3.18

# Non-root user
RUN addgroup -g 1001 appgroup && \
    adduser -D -u 1001 -G appgroup appuser

WORKDIR /app

# Dependencies only
COPY package*.json ./
RUN npm ci --only=production

# Copy app
COPY --chown=appuser:appgroup . .

# Run as non-root
USER appuser

# Health check
HEALTHCHECK --interval=30s CMD curl -f http://localhost:3000/health

EXPOSE 3000
CMD ["node", "src/index.js"]
```

## Security Best Practices

```yaml
# Docker Compose
services:
  app:
    image: myapp:1.0
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    read_only: true
    tmpfs:
      - /tmp
      - /run
    security_opt:
      - no-new-privileges:true
    user: "1001:1001"
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

## Kubernetes Security

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1001
  allowPrivilegeEscalation: false
  capabilities:
    drop:
      - ALL
  readOnlyRootFilesystem: true
```

## Image Scanning

```bash
# Trivy
trivy image --severity HIGH,CRITICAL myapp:1.0

# Grype
grype myapp:1.0

# Docker Scout
docker scout cves myapp:1.0
```

## Secrets Management

```bash
# Kubernetes Secrets
kubectl create secret generic db-creds \
  --from-literal=password=secret

# Docker Secrets (Swarm)
echo "secret" | docker secret create db-password -
```

## Key Practices

- Non-root users
- Minimal base images
- Read-only filesystems
- Capability dropping
- Resource limits
- Health checks
- Network policies
- Secret management
- Image scanning
- Regular updates

## Deployment Checklist

- [ ] No hardcoded secrets
- [ ] Image scanned for vulnerabilities
- [ ] Non-root user enforced
- [ ] Resource limits set
- [ ] Health checks defined
- [ ] Monitoring configured
- [ ] Logging enabled
- [ ] Network policies applied
- [ ] Backup strategy ready
- [ ] Disaster recovery tested
