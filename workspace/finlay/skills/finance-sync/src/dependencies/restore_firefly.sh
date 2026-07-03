#!/bin/bash
# restore_firefly.sh
# Purpose: Cleanly restore the Firefly III database on the remote server using a backup from the Synology share.
# Usage: ./restore_firefly.sh <backup_filename.tar.gz>

BACKUP_FILE=$1
REMOTE_HOST="openclaw@192.168.50.201"
REMOTE_BACKUP_DIR="/data/firefly/export"

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_filename.tar.gz>"
    echo "Example: $0 firefly_backup_20260423_235249.tar.gz"
    exit 1
fi

echo "Initiating remote restore of $BACKUP_FILE on $REMOTE_HOST..."

ssh -o StrictHostKeyChecking=no "$REMOTE_HOST" << EOF
    set -e

    echo "1. Extracting backup archive..."
    RESTORE_DIR=$(mktemp -d)
    tar --no-same-owner --no-same-permissions -xzf "$REMOTE_BACKUP_DIR/$BACKUP_FILE" -C "$RESTORE_DIR"

    echo "2. Stopping Firefly application container..."
    docker stop firefly_app

    echo "3. Dropping existing corrupted database and creating a clean slate..."
    docker exec -i firefly_db mariadb -ufirefly -psecret_firefly_password -e 'DROP DATABASE IF EXISTS firefly; CREATE DATABASE firefly;'

    echo "4. Streaming SQL dump into clean database..."
    cat "$RESTORE_DIR/db_dump.sql" | docker exec -i firefly_db mariadb -ufirefly -psecret_firefly_password firefly

    echo "5. Restarting Firefly application container..."
    docker start firefly_app

    echo "6. Cleaning up temporary files..."
    rm -rf "$RESTORE_DIR"

    echo "Restore completed successfully!"
EOF
