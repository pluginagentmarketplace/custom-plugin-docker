#!/bin/bash
# Docker Image Size Analyzer
# Compares image sizes and shows layer breakdown
# Usage: ./image-size-analyzer.sh <image1> [image2]

set -e

IMAGE1=${1:-}
IMAGE2=${2:-}

if [ -z "$IMAGE1" ]; then
    echo "Usage: $0 <image1> [image2]"
    echo "Example: $0 myapp:dev myapp:prod"
    exit 1
fi

echo "=========================================="
echo "Docker Image Size Analysis"
echo "=========================================="

analyze_image() {
    local IMAGE=$1
    echo ""
    echo "Image: $IMAGE"
    echo "----------------------------------------"

    # Get total size
    SIZE=$(docker images "$IMAGE" --format "{{.Size}}")
    echo "Total Size: $SIZE"

    # Show layer breakdown
    echo ""
    echo "Layer Breakdown:"
    docker history "$IMAGE" --format "{{.Size}}\t{{.CreatedBy}}" | \
        head -20 | \
        awk -F'\t' '{printf "%-10s %s\n", $1, substr($2, 1, 70)}'

    # Count layers
    LAYERS=$(docker history "$IMAGE" -q | wc -l)
    echo ""
    echo "Total Layers: $LAYERS"
}

analyze_image "$IMAGE1"

if [ -n "$IMAGE2" ]; then
    analyze_image "$IMAGE2"

    echo ""
    echo "=========================================="
    echo "Comparison"
    echo "=========================================="

    SIZE1=$(docker images "$IMAGE1" --format "{{.Size}}")
    SIZE2=$(docker images "$IMAGE2" --format "{{.Size}}")

    echo "$IMAGE1: $SIZE1"
    echo "$IMAGE2: $SIZE2"

    # Convert to bytes for comparison
    BYTES1=$(docker images "$IMAGE1" --format "{{.VirtualSize}}")
    BYTES2=$(docker images "$IMAGE2" --format "{{.VirtualSize}}")

    if [ "$BYTES2" -lt "$BYTES1" ]; then
        SAVED=$((BYTES1 - BYTES2))
        PERCENT=$((SAVED * 100 / BYTES1))
        echo ""
        echo "Savings: $PERCENT% reduction"
    fi
fi

echo ""
echo "=========================================="
echo "Optimization Tips"
echo "=========================================="
echo "1. Use multi-stage builds"
echo "2. Use alpine/slim base images"
echo "3. Combine RUN commands to reduce layers"
echo "4. Use .dockerignore to exclude files"
echo "5. Remove package manager caches"
echo "6. Don't install unnecessary packages"
