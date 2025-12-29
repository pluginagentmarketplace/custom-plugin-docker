#!/bin/bash
# Docker Volume Backup Script

VOLUME_NAME="${1:-mydata}"
BACKUP_DIR="${2:-./backups}"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

echo "Backing up volume: $VOLUME_NAME"

docker run --rm \
  -v "$VOLUME_NAME":/data:ro \
  -v "$BACKUP_DIR":/backup \
  alpine tar czf "/backup/${VOLUME_NAME}_${DATE}.tar.gz" -C /data .

echo "Backup created: $BACKUP_DIR/${VOLUME_NAME}_${DATE}.tar.gz"
