# Test Case: Batch Renamer Tool

## Purpose
Verify batch_rename.py works correctly with preview and apply modes.

## Setup Instructions

1. Create a test folder with sample files in /tmp or your home directory:
```bash
mkdir -p ./test-batch-rename
cd ./test-batch-rename
echo "Test file 1" > image_001.jpg
echo "Test file 2" > image_002.jpg  
echo "Test file 3" > image_003.jpg
echo "Document one" > document_backup_v1.txt
echo "Document two" > document_backup_v2.txt
```

2. Test preview mode:
```bash
python batch_rename.py --preview ./test-batch-rename "*.jpg" "PHOTO_"
# Should show preview of renaming image_001.jpg → PHOTO_image_001.jpg, etc.
```

3. Test apply mode (after seeing preview first!):
```bash
python batch_rename.py --apply ./test-batch-rename "*.jpg" "PHOTO_"
# Actually renames files if preview looked good
```

## Expected Behavior

### Preview Mode Should Show:
- List of all matching files
- New names for each file
- Total count of files to rename
- No actual changes made to filesystem

### Apply Mode Should Do:
- Rename each file as shown in preview
- Handle naming collisions by adding suffixes
- Report success/error counts at end
- Never modify if preview shows unexpected results

## Known Limitations (v1)

1. Pattern matching uses basic glob patterns - doesn't support complex regex yet
2. Number sequences need refinement to extract numbers from filenames properly
3. Unicode filenames may cause encoding issues on some systems
4. No undo functionality - always use --preview first!

## Future Improvements

- Add option for zero-padded numbering: `--number 5` to add `_0`, `_1`, etc.
- Support regex patterns instead of just glob wildcards
- Add dry-run flag that simulates without touching filesystem
- Create GUI version using tkinter or simple web interface
- Add logging to batch_rename.log file for audit trail

## Test Results

The tool has been tested with sample files and works correctly in both preview and apply modes. All basic functionality verified on Linux/macOS systems.

## Test Case 3: Special Characters in Filenames

### Setup
Create test files with spaces and unicode characters:
```bash
mkdir -p /tmp/test_special_chars
touch "/tmp/test_special_chars/summer vacation.jpg"
touch "/tmp/test_special_chars/münchen_bild.png"
touch "/tmp/test_special_chars/café_menu.pdf"
```

### Test Preview Mode
```bash
python3 batch_rename.py --preview /tmp/test_special_chars "*.jpg"
```
Expected: Shows files with spaces, warns about special characters.

### Test Apply Mode
```bash
python3 batch_rename.py --apply /tmp/test_special_chars "*.jpg" "VACATION_"
```
Expected: Renames successfully despite spaces in filename.

## Test Case 4: Unicode Error Handling

### Setup
Try to rename files from a path with unicode characters (if filesystem supports it):
```bash
mkdir -p "/tmp/été/test"
touch "/tmp/été/test/photo.jpg"
```

### Test
```bash
python3 batch_rename.py --preview /tmp/été "*.jpg"
```
Expected: Handles Unicode paths gracefully, shows warning if needed.
