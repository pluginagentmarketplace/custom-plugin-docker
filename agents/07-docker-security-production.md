---
description: Production-grade Docker security and best practices. Learn container security, image hardening, secrets management, monitoring, and production deployment patterns.
capabilities: ["Image security", "Container hardening", "Secrets management", "Network security", "Monitoring & logging", "Resource limits", "Health checks", "Backup strategies", "Disaster recovery"]
---

# 🐳 Docker Security & Production

## Overview
Enterprise-grade Docker security and production deployment patterns.

## Secure Dockerfile

```dockerfile
# Use specific base image version (not latest)
FROM alpine:3.18

# Install security updates
RUN apk update && apk upgrade

# Create non-root user
RUN addgroup -g 1001 appgroup && \
    adduser -D -u 1001 -G appgroup appuser

WORKDIR /app

# Copy files with correct ownership
COPY --chown=appuser:appgroup . .

# Install production dependencies only
RUN npm ci --only=production && \
    npm cache clean --force

# Remove build tools
RUN apk del gcc g++ make python3

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD node healthcheck.js

EXPOSE 3000

CMD ["node", "src/index.js"]
```

## Container Security Best Practices

```yaml
# Secure Docker Compose
version: '3.8'

services:
  app:
    image: myapp:1.0
    container_name: secure-app

    # Drop unnecessary capabilities
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE

    # Read-only root filesystem
    read_only: true

    # Temporary mount points
    tmpfs:
      - /tmp
      - /run

    # Resource limits
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M

    # Security options
    security_opt:
      - no-new-privileges:true

    # User
    user: "1001:1001"

    # Restart policy
    restart_policy:
      condition: on-failure
      delay: 5s
      max_attempts: 3
```

## Kubernetes Security Context

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-app
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1001
    runAsGroup: 1001
    fsGroup: 1001
    seccompProfile:
      type: RuntimeDefault

  containers:
  - name: app
    image: myapp:1.0

    securityContext:
      allowPrivilegeEscalation: false
      capabilities:
        drop:
          - ALL
      readOnlyRootFilesystem: true

    volumeMounts:
    - name: tmp
      mountPath: /tmp
    - name: run
      mountPath: /run

  volumes:
  - name: tmp
    emptyDir: {}
  - name: run
    emptyDir: {}
```

## Secrets Management

```bash
# Docker secrets (Swarm)
echo "database_password" | docker secret create db_password -
docker run --secret db_password myapp

# Kubernetes secrets
kubectl create secret generic db-credentials \
  --from-literal=password=secret123
kubectl create secret docker-registry regcred \
  --docker-server=registry.example.com \
  --docker-username=user \
  --docker-password=pass

# Environment secrets
# Never: docker run -e PASSWORD=secret
# Use: Docker Secrets or Kubernetes Secrets
```

## Image Scanning & Vulnerability Management

```bash
# Trivy deep scan
trivy image --severity HIGH,CRITICAL myapp:1.0

# Grype scanning
grype myapp:1.0

# Docker Scout
docker scout cves --only-severity high myapp:1.0

# Generate SBOM
trivy image --format cyclonedx myapp:1.0 > sbom.json
```

## Logging & Monitoring

```yaml
# docker-compose.yml with logging
services:
  app:
    image: myapp:1.0
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
        labels: "service=myapp,env=production"

    # Prometheus metrics endpoint
    ports:
      - "9090:9090"
```

## Production Deployment Checklist

```markdown
## Security
- [ ] Non-root user enforced
- [ ] Read-only filesystem (where possible)
- [ ] Capabilities dropped
- [ ] Privilege escalation disabled
- [ ] Security scanning passed
- [ ] No hardcoded secrets
- [ ] Secrets in vault/K8s secrets
- [ ] Image signed/verified

## Operations
- [ ] Resource limits set
- [ ] Health checks defined
- [ ] Restart policies configured
- [ ] Logging configured
- [ ] Monitoring in place
- [ ] Backup strategy defined
- [ ] Disaster recovery plan

## Deployment
- [ ] Multi-replica setup
- [ ] Load balancing configured
- [ ] Rolling update strategy
- [ ] Rollback capability
- [ ] Blue-green ready
- [ ] Canary ready
- [ ] Monitoring dashboard

## Network
- [ ] Egress filtering
- [ ] Network policies
- [ ] TLS/HTTPS enforced
- [ ] Port exposure minimized
- [ ] Service isolation
```

## Backup & Disaster Recovery

```bash
# Backup named volume
docker run --rm -v myvolume:/data -v $(pwd):/backup \
  alpine tar czf /backup/volume-backup.tar.gz /data

# Backup database in container
docker exec mydb pg_dump -U user dbname | \
  gzip > database-backup.sql.gz

# Restore volume
docker run --rm -v myvolume:/data -v $(pwd):/backup \
  alpine tar xzf /backup/volume-backup.tar.gz -C /

# Test recovery
docker run --rm -v backup-volume:/data alpine ls -la /data
```

## Network Security

```yaml
# Kubernetes network policies
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress

---
# Allow specific ingress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-web
spec:
  podSelector:
    matchLabels:
      app: web
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: prod
    ports:
    - protocol: TCP
      port: 3000
```

## Learning Path

### Beginner (15 hours)
1. Basic security concepts
2. Non-root users
3. Image scanning
4. Resource limits
5. Health checks

### Intermediate (20 hours)
1. Advanced security hardening
2. Secrets management
3. Network policies
4. Logging strategies
5. Monitoring setup

### Advanced (15 hours)
1. Zero-trust architecture
2. Compliance (CIS, PCI-DSS)
3. Advanced RBAC
4. Disaster recovery
5. Security auditing

## Best Practices

1. **Never run as root** (security)
2. **Scan all images** (vulnerability management)
3. **Use secrets management** (no hardcoding)
4. **Network policies** (segmentation)
5. **Resource limits** (DoS protection)
6. **Health checks** (reliability)
7. **Centralized logging** (audit trail)
8. **Regular backups** (disaster recovery)
9. **Monitoring alerts** (incident response)
10. **Regular patching** (security updates)
