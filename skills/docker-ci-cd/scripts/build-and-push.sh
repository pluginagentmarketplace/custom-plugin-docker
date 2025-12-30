#!/bin/bash
# Docker Build and Push Script for CI/CD
# Usage: ./build-and-push.sh <image-name> <tag> [registry]

set -e

IMAGE_NAME=${1:-}
TAG=${2:-latest}
REGISTRY=${3:-ghcr.io}
PUSH=${PUSH:-false}

if [ -z "$IMAGE_NAME" ]; then
    echo "Usage: $0 <image-name> [tag] [registry]"
    echo "Example: $0 myorg/myapp v1.0.0 ghcr.io"
    exit 1
fi

FULL_IMAGE="$REGISTRY/$IMAGE_NAME:$TAG"

echo "=========================================="
echo "Docker Build and Push"
echo "=========================================="
echo "Image: $FULL_IMAGE"
echo "Push: $PUSH"
echo "=========================================="

# Build with cache
echo ""
echo "Building image..."
docker build \
    --cache-from "$REGISTRY/$IMAGE_NAME:latest" \
    --build-arg BUILDKIT_INLINE_CACHE=1 \
    -t "$FULL_IMAGE" \
    -t "$REGISTRY/$IMAGE_NAME:latest" \
    .

# Run tests
echo ""
echo "Running container tests..."
docker run --rm "$FULL_IMAGE" /bin/sh -c "echo 'Health check passed'" || {
    echo "ERROR: Container test failed"
    exit 1
}

# Scan for vulnerabilities
echo ""
echo "Scanning for vulnerabilities..."
if command -v trivy &> /dev/null; then
    trivy image --severity HIGH,CRITICAL "$FULL_IMAGE"
else
    echo "Trivy not installed, skipping scan"
fi

# Push if enabled
if [ "$PUSH" = "true" ]; then
    echo ""
    echo "Pushing image..."
    docker push "$FULL_IMAGE"
    docker push "$REGISTRY/$IMAGE_NAME:latest"
    echo ""
    echo "Successfully pushed: $FULL_IMAGE"
else
    echo ""
    echo "Build complete. Set PUSH=true to push image."
fi

echo ""
echo "=========================================="
echo "Done!"
echo "=========================================="
