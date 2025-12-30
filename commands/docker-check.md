---
description: Check Docker installation, daemon status, and system health
allowed-tools: Bash
---

# /docker-check Command

Comprehensive Docker environment health check and diagnostics.

## Usage

```
/docker-check [--verbose]
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| --verbose | No | false | Show detailed output |

## Checks Performed

### 1. Docker Engine
- Docker version and API version
- Daemon status (running/stopped)
- Storage driver
- Cgroup driver

### 2. Docker Compose
- Compose version
- Compose V2 availability

### 3. System Resources
- Disk usage (`docker system df`)
- Available disk space
- Memory available
- CPU cores

### 4. Container Status
- Running containers count
- Stopped containers count
- Container health status

### 5. Image Status
- Total images
- Dangling images
- Space used by images

### 6. Network Status
- Available networks
- Custom networks

### 7. Volume Status
- Total volumes
- Unused volumes

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All checks passed |
| 1 | Docker not installed |
| 2 | Docker daemon not running |
| 3 | Resource warnings |

## Example Output

```
Docker Environment Check
========================

Docker Engine:
  ✓ Version: 24.0.7
  ✓ API: 1.43
  ✓ Daemon: running
  ✓ Storage: overlay2

Docker Compose:
  ✓ Version: 2.23.0

System Resources:
  ✓ Disk: 45GB free (70% used)
  ✓ Memory: 8GB available
  ✓ CPU: 4 cores

Containers:
  ✓ Running: 3
  ✓ Stopped: 2
  ✓ All healthy

Images:
  ✓ Total: 15
  ⚠ Dangling: 5 (clean with: docker image prune)

Recommendations:
  - Remove dangling images to free 2.3GB
  - Remove stopped containers
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Docker not running | `sudo systemctl start docker` |
| Permission denied | Add user to docker group |
| Low disk space | `docker system prune -a` |
