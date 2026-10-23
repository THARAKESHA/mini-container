#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
ROOTFS_DIR="$PROJECT_DIR/rootfs"

echo "=== Setting up Root Filesystem for Mini-Container ==="
if [ -f "$ROOTFS_DIR/bin/sh" ]; then
    echo "Root filesystem already present at $ROOTFS_DIR"
    exit 0
fi

mkdir -p "$ROOTFS_DIR"
cd "$ROOTFS_DIR"

ALPINE_VERSION="3.20.0"
TAR_FILE="alpine-minirootfs-${ALPINE_VERSION}-x86_64.tar.gz"
URL="https://dl-cdn.alpinelinux.org/alpine/v3.20/releases/x86_64/${TAR_FILE}"

echo "Downloading minimal root filesystem ($TAR_FILE ~ 3.5MB)..."
curl -sSL "$URL" -o "$TAR_FILE"

echo "Extracting root filesystem..."
tar -xzf "$TAR_FILE"
rm -f "$TAR_FILE"

# Create proc mount point
mkdir -p proc dev sys

echo "Root filesystem successfully prepared at: $ROOTFS_DIR"
echo "Contains POSIX utilities: /bin/sh, /bin/ls, /bin/ps, etc."
