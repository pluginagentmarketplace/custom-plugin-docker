#!/bin/bash
# Docker Private Registry Setup Script
# Version: 1.0.0
# Usage: ./registry-setup.sh [--with-auth] [--with-tls]

set -e

REGISTRY_PORT=${REGISTRY_PORT:-5000}
REGISTRY_DIR=${REGISTRY_DIR:-/var/lib/registry}
WITH_AUTH=false
WITH_TLS=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --with-auth) WITH_AUTH=true; shift ;;
        --with-tls) WITH_TLS=true; shift ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

echo "=========================================="
echo "Docker Private Registry Setup"
echo "=========================================="
echo "Port: $REGISTRY_PORT"
echo "Data Directory: $REGISTRY_DIR"
echo "Authentication: $WITH_AUTH"
echo "TLS: $WITH_TLS"
echo "=========================================="

# Create directories
mkdir -p "$REGISTRY_DIR"
mkdir -p ./auth
mkdir -p ./certs

# Setup authentication if requested
if [ "$WITH_AUTH" = true ]; then
    echo ""
    echo "Setting up authentication..."

    if ! command -v htpasswd &> /dev/null; then
        echo "Installing apache2-utils for htpasswd..."
        apt-get update && apt-get install -y apache2-utils
    fi

    read -p "Enter username: " USERNAME
    read -s -p "Enter password: " PASSWORD
    echo ""

    htpasswd -Bbn "$USERNAME" "$PASSWORD" > ./auth/htpasswd
    echo "Authentication configured for user: $USERNAME"
fi

# Generate self-signed certificate if TLS requested
if [ "$WITH_TLS" = true ]; then
    echo ""
    echo "Generating self-signed certificate..."

    openssl req -newkey rsa:4096 -nodes -sha256 \
        -keyout ./certs/domain.key \
        -x509 -days 365 \
        -out ./certs/domain.crt \
        -subj "/CN=localhost"

    echo "TLS certificate generated"
fi

# Build docker run command
RUN_CMD="docker run -d --name registry --restart=always"
RUN_CMD="$RUN_CMD -p $REGISTRY_PORT:5000"
RUN_CMD="$RUN_CMD -v $REGISTRY_DIR:/var/lib/registry"
RUN_CMD="$RUN_CMD -e REGISTRY_STORAGE_DELETE_ENABLED=true"

if [ "$WITH_AUTH" = true ]; then
    RUN_CMD="$RUN_CMD -v $(pwd)/auth:/auth"
    RUN_CMD="$RUN_CMD -e REGISTRY_AUTH=htpasswd"
    RUN_CMD="$RUN_CMD -e REGISTRY_AUTH_HTPASSWD_REALM=Registry"
    RUN_CMD="$RUN_CMD -e REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd"
fi

if [ "$WITH_TLS" = true ]; then
    RUN_CMD="$RUN_CMD -v $(pwd)/certs:/certs"
    RUN_CMD="$RUN_CMD -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt"
    RUN_CMD="$RUN_CMD -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key"
fi

RUN_CMD="$RUN_CMD registry:2"

# Stop existing registry if running
docker stop registry 2>/dev/null || true
docker rm registry 2>/dev/null || true

# Start registry
echo ""
echo "Starting registry..."
eval "$RUN_CMD"

# Verify
sleep 2
if docker ps | grep -q registry; then
    echo ""
    echo "=========================================="
    echo "Registry started successfully!"
    echo "=========================================="
    echo ""
    echo "Usage:"
    echo "  Tag:  docker tag myimage localhost:$REGISTRY_PORT/myimage"
    echo "  Push: docker push localhost:$REGISTRY_PORT/myimage"
    echo "  Pull: docker pull localhost:$REGISTRY_PORT/myimage"
    echo ""
    if [ "$WITH_AUTH" = true ]; then
        echo "Login: docker login localhost:$REGISTRY_PORT"
    fi
else
    echo "ERROR: Registry failed to start"
    docker logs registry
    exit 1
fi
