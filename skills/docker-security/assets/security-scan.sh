#!/bin/bash
# Docker Security Scan Script

IMAGE="${1:-myapp:latest}"

echo "=== Docker Security Scan ==="
echo "Image: $IMAGE"
echo ""

# Docker Scout (if available)
if command -v docker &> /dev/null; then
    echo "=== Docker Scout CVE Scan ==="
    docker scout cves "$IMAGE" 2>/dev/null || echo "Docker Scout not available"
fi

# Trivy (if available)
if command -v trivy &> /dev/null; then
    echo ""
    echo "=== Trivy Vulnerability Scan ==="
    trivy image --severity HIGH,CRITICAL "$IMAGE"
fi

echo ""
echo "=== Image Details ==="
docker inspect "$IMAGE" --format='User: {{.Config.User}}'
docker inspect "$IMAGE" --format='Healthcheck: {{.Config.Healthcheck}}'
