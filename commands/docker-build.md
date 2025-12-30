---
description: Build Docker image with best practices, optimization, and security scanning
allowed-tools: Bash, Read, Write
---

# /docker-build Command

Build optimized Docker image with best practices validation and security scanning.

## Usage

```
/docker-build [Dockerfile path] [options]
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| path | No | ./Dockerfile | Path to Dockerfile |
| --tag | No | app:latest | Image tag |
| --scan | No | true | Run security scan |

## Workflow

1. **Validate Dockerfile**
   - Check syntax errors
   - Verify base image exists
   - Lint with hadolint rules

2. **Check .dockerignore**
   - Verify exists
   - Suggest additions (node_modules, .git, etc.)

3. **Build with Optimization**
   - Enable BuildKit (`DOCKER_BUILDKIT=1`)
   - Use cache mounts where applicable
   - Multi-platform support

4. **Analyze Result**
   - Show final image size
   - Display layer breakdown
   - Compare with base image

5. **Security Scan**
   - Run Trivy/Docker Scout
   - Report vulnerabilities by severity
   - Suggest remediations

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Dockerfile validation failed |
| 2 | Build failed |
| 3 | Critical vulnerabilities found |

## Example Output

```
✓ Dockerfile validated
✓ .dockerignore configured (12 patterns)
✓ Building with BuildKit...
✓ Image built: myapp:latest (145MB)

Layer Analysis:
  base: 45MB (node:20-alpine)
  deps: 80MB (node_modules)
  app:  20MB (source code)

Security Scan:
  CRITICAL: 0
  HIGH: 2 (fixable)
  MEDIUM: 5

Recommendations:
  - Update base image to node:20.10-alpine
  - Add USER instruction for non-root
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Build context too large | Add patterns to .dockerignore |
| Cache not working | Check layer order (deps before code) |
| Permission denied | Run with sudo or add user to docker group |
