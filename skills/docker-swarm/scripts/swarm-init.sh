#!/bin/bash
# Docker Swarm Cluster Initialization Script
# Usage: ./swarm-init.sh [--advertise-addr IP]

set -e

ADVERTISE_ADDR=${ADVERTISE_ADDR:-}

echo "=========================================="
echo "Docker Swarm Initialization"
echo "=========================================="

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --advertise-addr) ADVERTISE_ADDR="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

# Check if already in swarm
if docker info 2>/dev/null | grep -q "Swarm: active"; then
    echo "This node is already part of a Swarm"
    docker node ls
    exit 0
fi

# Initialize swarm
echo "Initializing Swarm cluster..."
if [ -n "$ADVERTISE_ADDR" ]; then
    docker swarm init --advertise-addr "$ADVERTISE_ADDR"
else
    docker swarm init
fi

# Get join tokens
echo ""
echo "=========================================="
echo "Swarm initialized successfully!"
echo "=========================================="

echo ""
echo "To add a WORKER node, run this command:"
echo "----------------------------------------"
docker swarm join-token worker 2>/dev/null | grep "docker swarm join"

echo ""
echo "To add a MANAGER node, run this command:"
echo "----------------------------------------"
docker swarm join-token manager 2>/dev/null | grep "docker swarm join"

# Create default networks
echo ""
echo "Creating default networks..."
docker network create --driver overlay --attachable frontend 2>/dev/null || true
docker network create --driver overlay --internal backend 2>/dev/null || true

echo ""
echo "=========================================="
echo "Swarm Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Add worker nodes using the join token above"
echo "2. Deploy your stack: docker stack deploy -c stack.yaml myapp"
echo "3. View services: docker service ls"
echo "4. View nodes: docker node ls"
