---
name: docker-cicd
description: Docker in CI/CD pipelines. Learn automated builds, testing in containers, registry integration, and deployment automation with GitHub Actions and other CI/CD tools. Use when automating Docker workflows.
---

# Docker CI/CD

Automate Docker builds and deployments.

## GitHub Actions

```yaml
name: Docker Build & Push

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Build and push
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: username/myapp:latest

    - name: Test image
      run: docker run --rm username/myapp:latest npm test
```

## Multi-Stage Pipeline

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - run: docker build --target test -t myapp:test . && docker run myapp:test

  build:
    needs: test
    steps:
    - run: docker build -t username/myapp:latest .

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    steps:
    - run: ssh deploy@server docker pull username/myapp:latest
```

## Image Scanning

```bash
# Trivy
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy:latest image myapp:latest

# Docker Scout
docker scout cves myapp:latest
```

## Dockerfile for Testing

```dockerfile
FROM node:18-alpine AS test
COPY . .
RUN npm ci && npm test

FROM node:18-alpine AS production
COPY src ./src
CMD ["node", "src/index.js"]
```

## Key Workflows

- Build on push
- Test in containers
- Push to registry
- Deploy to production
- Scan for vulnerabilities
- Multi-stage builds
- Tagged releases
- Artifact storage

## Best Practices

1. Automated testing
2. Image scanning
3. Version tagging
4. Progressive deployment
5. Rollback capability
6. Environment separation
7. Monitoring alerts
8. Deployment logs
