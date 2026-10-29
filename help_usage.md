# Batch Renamer - Usage Guide

## Quick Start (3 Steps)

### Step 1: Preview what will change
```bash
python batch_rename.py --preview ./target-folder "*.jpg" "PHOTO_"
```

This shows you exactly which files will be renamed and to what new names. **READ THIS CAREFULLY!** If anything looks wrong, abort before proceeding.

### Step 2: Apply only if preview looked good
```bash
python batch_rename.py --apply ./target-folder "*.jpg" "PHOTO_"
```

This actually renames the files as shown in the preview. Only use this after you're confident the changes are correct!

### Step 3: Check results
List the folder contents to verify renaming worked:
```bash
ls -la ./target-folder/
```

---

## Common Use Cases

### Case 1: Rename all photos with uppercase prefix
Your folder has `vacation_001.jpg`, `vacation_002.jpg`, etc. You want to rename them to `PHOTO_vacation_001.jpg`.

**Command:**
```bash
python batch_rename.py --preview ./photos "*.jpg" "PHOTO_"
# See preview, then add --apply when ready
```

### Case 2: Number backup files sequentially
Your backups are named `data_backup.txt`, `config_backup.txt` but you want them numbered.

**Command:**
```bash
python batch_rename.py --preview ./backups "*backup*" "_0"
# Shows preview with _0, _1, _2 numbering added
```

### Case 3: Rename all documents to uppercase
Documents like `my_report.pdf` → `MY_REPORT.pdf`:

**Command:**
```bash
python batch_rename.py --preview ./docs "*.pdf" "UPPER_"
# Note: This just adds prefix - for true case conversion see next section
```

---

## Advanced Usage

### Zero-Padded Numbering

To automatically number files from 0 to N-1 with zero-padding (e.g., `_0`, `_01`, `_02`):

**Command:**
```bash
python batch_rename.py --number 5 ./photos "*.jpg" "IMG_"
# Will rename up to 5 files, numbering them _0, _1, _2, etc.
```

### Renaming with Specific Pattern Replacement

If you want to replace a specific part of the filename (not just add prefix):

**Example:** Rename `image_2023_001.jpg` → `IMG_2023_001.jpg`:

**Command:**
```bash
python batch_rename.py --preview ./photos "image_*" "IMG_"
# This replaces the matched pattern with new prefix
```

---

## Safety Rules (READ THESE!)

1. **ALWAYS use --preview first!** Never skip preview mode unless you know exactly what will happen.
2. **Never use --apply without seeing preview results.** If preview shows unexpected changes, fix your command before applying.
3. **Check file permissions** - make sure you can write to the target folder.
4. **Backup important data** before running batch operations on critical files.
5. **Test with a small subset first** if renaming many files in an important directory.

---

## Troubleshooting

### "No files found matching pattern"
- Check that your glob pattern is correct (use `*` for wildcards)
- Make sure you're using the right folder path
- Try simpler patterns like `"*.txt"` to test first

### Files not renaming as expected
- The new filename must be unique - if two files would get the same name, it will fail
- Check that your prefix doesn't create duplicate names with existing files
- Use `--number N` option to add sequential numbering and avoid collisions

### Permission errors
```bash
# Make sure you have write access:
ls -la ./target-folder/
# If needed, run as root or fix permissions:
sudo chmod u+w ./target-folder/
```

---

## Examples for Different Scenarios

### Photographers organizing vacation photos:
```bash
python batch_rename.py --preview ./vacation_photos/*.jpg "VACATION_"
```

### Developers renaming log files chronologically:
```bash
python batch_rename.py --apply ./logs "*.log" "LOG_"
# Renames app.log → LOG_app_1.log, error.log → LOG_error_2.log, etc.
```

### Media managers converting filenames to uppercase:
**Note:** Current version only adds prefixes - for full case conversion you'd need additional Python code using `str.upper()` on the filename string before renaming.

---

## Limitations (v1)

- Works with standard file systems and common extensions
- Pattern matching uses glob wildcards (`*`, `[...]`) not regex
- No built-in undo - always preview first!
- Unicode filenames may behave unexpectedly depending on system locale settings
- Large folders (>10,000 files) might be slow to scan

---

## Future Versions (v2+)

Planned improvements:
- True case conversion option (--uppercase/--lowercase flags)
- Regex pattern support for more flexible matching
- Undo/rollback functionality with timestamp logging
- GUI interface using tkinter or web-based dashboard
- Integration with file managers via desktop icons
- Batch compression after renaming (zip folders by name pattern)

---

*Created by Wisp the digital spirit | MIT License - use freely and improve!*