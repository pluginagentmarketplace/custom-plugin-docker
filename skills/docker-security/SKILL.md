---
name: docker-security
description: Master Docker security - image scanning, runtime security, secrets, and container hardening
sasmp_version: "1.3.0"
bonded_agent: docker-security
bond_type: PRIMARY_BOND
---

# Docker Security Skill

## Image Security

```bash
# Scan for vulnerabilities
docker scout cves myimage
trivy image myimage

# Use minimal base
FROM alpine:3.19
FROM gcr.io/distroless/static
```

## Runtime Security

```bash
# Non-root user
docker run --user 1001 myapp

# Read-only filesystem
docker run --read-only myapp

# Drop capabilities
docker run --cap-drop=ALL myapp

# No new privileges
docker run --security-opt=no-new-privileges myapp
```

## Secrets Management

```bash
# Docker secrets (Swarm)
echo "password" | docker secret create db_pass -
docker service create --secret db_pass myapp

# Compose secrets
secrets:
  db_pass:
    file: ./secrets/db_pass.txt
```

## Assets
- `security-scan.sh` - Scanning script

## References
- `SECURITY_GUIDE.md` - Best practices
