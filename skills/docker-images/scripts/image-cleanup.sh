#!/bin/bash
# Docker Image Cleanup Script

echo "=== Docker Image Cleanup ==="

echo "Dangling images:"
docker images -f dangling=true

echo ""
echo "Removing dangling images..."
docker image prune -f

echo ""
echo "Images older than 30 days:"
docker images --format "{{.Repository}}:{{.Tag}} {{.CreatedSince}}" | grep -E "(months|weeks)" | head -10

echo ""
echo "Total disk usage:"
docker system df

echo ""
echo "To remove all unused images: docker image prune -a"
