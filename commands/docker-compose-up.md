---
description: Start Docker Compose services with validation, health monitoring, and status reporting
allowed-tools: Bash
---

# /docker-compose-up Command

Start Docker Compose services with intelligent validation and monitoring.

## Usage

```
/docker-compose-up [compose file] [options]
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| file | No | docker-compose.yaml | Compose file path |
| --build | No | false | Rebuild images |
| --detach | No | true | Run in background |
| --wait | No | true | Wait for health checks |

## Workflow

### 1. Pre-flight Validation
- Validate YAML syntax
- Check service definitions
- Verify image availability
- Validate network/volume references

### 2. Environment Check
- Load .env file
- Validate required variables
- Check for secrets

### 3. Start Services
- Pull required images
- Build if needed
- Start in dependency order
- Apply health check waits

### 4. Health Monitoring
- Wait for all health checks
- Report service status
- Show connection info

### 5. Status Report
- Running services
- Exposed ports
- Log access commands

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All services healthy |
| 1 | Compose file invalid |
| 2 | Image pull failed |
| 3 | Service failed to start |
| 4 | Health check timeout |

## Example Output

```
Docker Compose Up
=================

Pre-flight:
  ✓ Compose file valid
  ✓ 3 services defined
  ✓ .env loaded (5 variables)

Starting Services:
  ✓ database: pulling postgres:16-alpine
  ✓ database: started (waiting for health)
  ✓ database: healthy
  ✓ backend: building...
  ✓ backend: started (waiting for health)
  ✓ backend: healthy
  ✓ frontend: started
  ✓ frontend: healthy

Services Running:
  ┌─────────┬────────────┬───────────────┐
  │ Service │ Status     │ Ports         │
  ├─────────┼────────────┼───────────────┤
  │ frontend│ healthy    │ 80->80        │
  │ backend │ healthy    │ 3000 (internal)│
  │ database│ healthy    │ 5432 (internal)│
  └─────────┴────────────┴───────────────┘

Access:
  Frontend: http://localhost:80

Logs:
  docker compose logs -f
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port already in use | Change port in compose file |
| Image not found | Check image name and registry |
| Health check timeout | Increase start_period |
| Service dependency fail | Check depends_on conditions |
