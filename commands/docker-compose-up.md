---
description: Start Docker Compose services with health checks
allowed-tools: Bash
---

# /docker-compose-up Command

Start Docker Compose services intelligently.

## Usage

```
/docker-compose-up [compose file]
```

## What It Does

1. Validates compose file
2. Checks for required images
3. Starts services
4. Waits for health checks
5. Shows service status
