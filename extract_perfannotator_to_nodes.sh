#!/bin/bash
set -euo pipefail

# Configuration
ARCHIVE_PATH="/nfs/perfannotator-mini.tgz"
TARGET_DIR="/users/akazad"
EXTRACTION_DIR="fine_tuned_graphcodebert_best_170K"

echo "Extracting perfannotator-mini.tgz to all client nodes..."
echo "Archive: $ARCHIVE_PATH ($(du -h $ARCHIVE_PATH | cut -f1))"
echo "Target: $TARGET_DIR/$EXTRACTION_DIR"
echo "Nodes: $(wc -l < sshhosts) clients"
echo ""

# Verify NFS mount and archive exists on all nodes first
echo "Step 1: Verifying NFS access on all nodes..."
parallel-ssh -h sshhosts -p 20 -t 30 -i "test -f $ARCHIVE_PATH && echo 'NFS OK' || echo 'NFS FAILED'"

echo ""
echo "Step 2: Creating target directories on all nodes..."
parallel-ssh -h sshhosts -p 20 -t 30 -i "mkdir -p $TARGET_DIR"

echo ""
echo "Step 3: Extracting archive on all nodes (this may take a few minutes)..."
echo "Command: tar -xzf $ARCHIVE_PATH -C $TARGET_DIR"

# Extract with progress monitoring
parallel-ssh -h sshhosts -p 10 -t 600 -i \
  "cd $TARGET_DIR && tar -xzf $ARCHIVE_PATH && echo 'Extraction completed on \$(hostname)'"

echo ""
echo "Step 4: Verifying extraction on all nodes..."
parallel-ssh -h sshhosts -p 20 -t 30 -i \
  "test -d $TARGET_DIR/$EXTRACTION_DIR && echo 'SUCCESS: \$(ls $TARGET_DIR/$EXTRACTION_DIR | wc -l) files extracted' || echo 'FAILED: Directory not found'"

echo ""
echo "Step 5: Checking model file sizes..."
parallel-ssh -h sshhosts -p 20 -t 30 -i \
  "du -sh $TARGET_DIR/$EXTRACTION_DIR 2>/dev/null | head -1 || echo 'Size check failed'"

echo ""
echo "Extraction process completed!"
echo ""
echo "To verify manually on a specific node:"
echo "  ssh <node-ip> 'ls -la $TARGET_DIR/$EXTRACTION_DIR/'"