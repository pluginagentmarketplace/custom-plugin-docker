---
name: docker-registries
description: Master Docker registries - Docker Hub, private registries, tagging, and CI/CD integration
sasmp_version: "1.3.0"
bonded_agent: docker-registries
bond_type: PRIMARY_BOND
---

# Docker Registries Skill

## Docker Hub

```bash
docker login
docker push myuser/myapp:v1
docker pull myuser/myapp:v1
```

## Private Registry

```bash
# Run local registry
docker run -d -p 5000:5000 registry:2

# Push to local
docker tag myapp localhost:5000/myapp
docker push localhost:5000/myapp
```

## Cloud Registries

### AWS ECR
```bash
aws ecr get-login-password | docker login --username AWS --password-stdin 123456.dkr.ecr.us-east-1.amazonaws.com
```

### GCR
```bash
gcloud auth configure-docker
docker push gcr.io/project/image
```

## Tagging Strategy

```bash
myapp:v1.2.3    # Semantic version
myapp:abc123f   # Git SHA
myapp:latest    # Avoid in production!
```

## Assets
- `ci-docker.yml` - GitHub Actions workflow

## References
- `REGISTRY_GUIDE.md` - Best practices
