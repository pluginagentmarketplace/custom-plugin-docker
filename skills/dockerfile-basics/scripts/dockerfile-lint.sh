#!/bin/bash
# Dockerfile Linter using Hadolint
# Usage: ./dockerfile-lint.sh [Dockerfile]

DOCKERFILE=${1:-Dockerfile}

if ! command -v hadolint &> /dev/null; then
    echo "Running hadolint via Docker..."
    docker run --rm -i hadolint/hadolint < "$DOCKERFILE"
else
    hadolint "$DOCKERFILE"
fi
