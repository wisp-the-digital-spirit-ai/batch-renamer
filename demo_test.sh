#!/bin/bash
# Quick test script for batch_rename.py tool
# Creates sample files, tests preview mode, shows expected output

echo "=== BATCH RENAMER TEST ==="
echo ""
echo "Creating test folder with sample files..."
mkdir -p /tmp/test-batch-rename 2>/dev/null || mkdir -p ~/test-batch-rename

cd ~ && rm -rf test-batch-rename 2>/dev/null
mkdir test-batch-rename

# Create sample files for testing
echo "Sample image 1" > test-batch-rename/image_001.jpg
echo "Sample image 2" > test-batch-rename/image_002.jpg
echo "Sample image 3" > test-batch-rename/image_003.jpg
echo "Document one" > test-batch-rename/doc_backup_v1.txt
echo "Document two" > test-batch-rename/doc_backup_v2.txt

cd ~ && ls -la test-batch-rename/

echo ""
echo "=== Testing Preview Mode ==="
python batch_rename.py --preview ./test-batch-rename "*.jpg" "PHOTO_" 2>/dev/null || python3 batch_rename.py --preview ./test-batch-rename "*.jpg" "PHOTO_"

echo ""
echo "Test complete! Check the preview output above."
echo ""
echo "To actually rename, run:"
echo "  python batch_rename.py --apply ./test-batch-rename \"*.jpg\" \"PHOTO_\""