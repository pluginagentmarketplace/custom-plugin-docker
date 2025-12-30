# Docker CI/CD Integration Guide

## GitHub Actions

### Basic Build and Push
```yaml
- name: Build and push
  uses: docker/build-push-action@v5
  with:
    push: true
    tags: user/app:latest
```

### Multi-Platform Build
```yaml
- uses: docker/setup-qemu-action@v3
- uses: docker/setup-buildx-action@v3
- uses: docker/build-push-action@v5
  with:
    platforms: linux/amd64,linux/arm64
```

### Cache Configuration
```yaml
cache-from: type=gha
cache-to: type=gha,mode=max
```

## GitLab CI

### Basic Pipeline
```yaml
build:
  image: docker:24
  services:
    - docker:dind
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
```

## Security Scanning

### Trivy Integration
```yaml
- name: Trivy scan
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: myapp:latest
    format: sarif
```

### Snyk Integration
```yaml
- name: Snyk Container
  uses: snyk/actions/docker@master
  with:
    image: myapp:latest
```

## Best Practices

1. **Use semantic versioning** for image tags
2. **Scan all images** before pushing
3. **Cache layers** for faster builds
4. **Multi-arch support** for ARM compatibility
5. **Sign images** for supply chain security
6. **Automate** everything possible

## Environment Variables

```bash
# Common CI/CD variables
DOCKER_BUILDKIT=1
DOCKER_CLI_EXPERIMENTAL=enabled
COMPOSE_DOCKER_CLI_BUILD=1
```
