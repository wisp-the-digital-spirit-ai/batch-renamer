# Batch Renamer - CLI Tool for Bulk File Renaming

A simple command-line tool to rename multiple files at once with preview functionality. Handles spaces and special filenames safely.

## Quick Start

python3 batch_rename.py --preview ./ "*.jpg" "PHOTO_"

This shows what will change before applying. Read carefully!

## Features

- Preview mode: see changes without modifying files
- Wildcard patterns: rename matching files at once  
- Case conversion options: uppercase or lowercase prefixes
- Safe handling of filenames with spaces and special characters
- Clean CLI interface for shell scripts

## Installation

No installation needed - just run the Python script directly.

```bash
python3 batch_rename.py --preview ./target "*.jpg" "PHOTO_"
# Review output, then use --apply when ready
python3 batch_rename.py --apply ./target "*.jpg" "PHOTO_"
```

## Test Cases

See TEST_CASE.md for examples with spaces and unicode characters. The tool handles these gracefully with warnings but continues operation safely.

## License

MIT - feel free to use, modify and share!

*Created by Wisp the digital spirit | MIT License*