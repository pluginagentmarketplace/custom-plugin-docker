---
description: Build Docker image with best practices
allowed-tools: Bash, Read, Write
---

# /docker-build Command

Build optimized Docker image for your application.

## Usage

```
/docker-build [Dockerfile path]
```

## What It Does

1. Validates Dockerfile
2. Checks .dockerignore
3. Builds with cache optimization
4. Shows image size
5. Suggests improvements
