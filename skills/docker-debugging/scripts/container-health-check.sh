#!/bin/bash
# Container Health Check Script
# Version: 1.0.0
# Usage: ./container-health-check.sh <container_id_or_name>

set -e

CONTAINER=${1:-}

if [ -z "$CONTAINER" ]; then
    echo "Usage: $0 <container_id_or_name>"
    exit 1
fi

echo "=========================================="
echo "Container Health Check Report"
echo "Container: $CONTAINER"
echo "Date: $(date)"
echo "=========================================="

# Check if container exists
if ! docker inspect "$CONTAINER" > /dev/null 2>&1; then
    echo "ERROR: Container '$CONTAINER' not found"
    exit 1
fi

# Basic Info
echo ""
echo "--- Basic Information ---"
docker inspect --format='Name: {{.Name}}' "$CONTAINER"
docker inspect --format='Image: {{.Config.Image}}' "$CONTAINER"
docker inspect --format='Status: {{.State.Status}}' "$CONTAINER"
docker inspect --format='Started: {{.State.StartedAt}}' "$CONTAINER"

# Health Status
echo ""
echo "--- Health Status ---"
HEALTH=$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}no healthcheck{{end}}' "$CONTAINER")
echo "Health: $HEALTH"

if [ "$HEALTH" != "no healthcheck" ]; then
    echo "Last Health Check:"
    docker inspect --format='{{range $i, $h := .State.Health.Log}}{{if eq $i 0}}Exit: {{$h.ExitCode}} - {{$h.Output}}{{end}}{{end}}' "$CONTAINER" 2>/dev/null || echo "No health log available"
fi

# Resource Usage
echo ""
echo "--- Resource Usage ---"
docker stats "$CONTAINER" --no-stream --format "CPU: {{.CPUPerc}} | Memory: {{.MemUsage}} | Net I/O: {{.NetIO}} | Block I/O: {{.BlockIO}}"

# Network Info
echo ""
echo "--- Network Configuration ---"
docker inspect --format='{{range $net, $conf := .NetworkSettings.Networks}}Network: {{$net}} | IP: {{$conf.IPAddress}}{{end}}' "$CONTAINER"

# Port Mappings
echo ""
echo "--- Port Mappings ---"
docker port "$CONTAINER" 2>/dev/null || echo "No ports exposed"

# Recent Logs
echo ""
echo "--- Recent Logs (last 10 lines) ---"
docker logs --tail 10 "$CONTAINER" 2>&1

# Running Processes
echo ""
echo "--- Running Processes ---"
docker top "$CONTAINER" 2>/dev/null || echo "Unable to get process list"

echo ""
echo "=========================================="
echo "Health Check Complete"
echo "=========================================="
