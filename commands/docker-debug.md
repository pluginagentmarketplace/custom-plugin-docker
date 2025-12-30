---
description: Debug Docker containers and troubleshoot issues with comprehensive diagnostics
allowed-tools: Bash
---

# /docker-debug Command

Comprehensive container debugging and issue diagnosis.

## Usage

```
/docker-debug <container> [--issue <type>]
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| container | Yes | - | Container name or ID |
| --issue | No | all | crash/network/resource/health |

## Diagnostics Performed

### 1. Container State
- Current status (running/stopped/restarting)
- Exit code analysis
- Restart count
- Uptime

### 2. Logs Analysis
- Last 100 log lines
- Error pattern detection
- Stack trace identification

### 3. Resource Usage
- CPU percentage
- Memory usage vs limit
- I/O statistics
- Network I/O

### 4. Health Check
- Health status
- Last health check output
- Health check configuration

### 5. Network Connectivity
- Assigned networks
- IP addresses
- Port mappings
- DNS resolution test

### 6. Volume Mounts
- Mounted volumes
- Permission status
- Mount path validation

### 7. Environment
- Environment variables (sanitized)
- Entrypoint/CMD
- Working directory

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Container healthy |
| 1 | Container not found |
| 2 | Container crashed |
| 3 | Health check failing |
| 4 | Resource issues |
| 5 | Network issues |

## Exit Code Reference

| Container Exit | Meaning | Action |
|----------------|---------|--------|
| 0 | Normal exit | Check if expected |
| 1 | Application error | Check logs |
| 137 | OOMKilled | Increase memory |
| 139 | Segfault | Check application |
| 143 | SIGTERM | Graceful shutdown |

## Example Output

```
Container Debug: my-app
=======================

State:
  ✗ Status: restarting
  ✗ Exit Code: 137 (OOMKilled)
  ⚠ Restarts: 5

Resources:
  ✗ Memory: 512MB/512MB (100%) - LIMIT HIT
  ✓ CPU: 45%

Last Logs:
  [ERROR] Out of memory
  [ERROR] Cannot allocate buffer

Health Check:
  ✗ Status: unhealthy
  ✗ Last Check: "connection refused"

Network:
  ✓ IP: 172.17.0.5
  ✓ Ports: 3000->3000

Diagnosis:
  Container is being OOMKilled due to memory limit.

Recommendations:
  1. Increase memory limit: --memory=1g
  2. Check for memory leaks in application
  3. Profile memory usage
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Container not found | Use `docker ps -a` to list all |
| Permission denied | Check volume ownership |
| Network unreachable | Verify network membership |
