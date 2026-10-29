# Changelog for Batch Renamer

## 2026-10-29: Added Unicode and Special Character Handling

### Improvements
- Added error handling for Unicode paths and filenames (spaces, non-ASCII characters)
- Improved OSError handling in apply_rename function  
- Added warnings when destination paths contain spaces or special characters
- Enhanced preview mode to warn about problematic characters before renaming

### Files Changed
- `batch_rename.py`: Appended improved functions with better error handling for unicode/special chars
- `README.md`: Updated documentation with new features and limitations
- `TEST_CASE.md`: Added test cases for special character handling
- `test_special.sh`: New script to quickly test special character scenarios

### Known Issues (Addressed)
- Previously: No explicit handling for UnicodeEncodeError or paths with spaces
- Now: Graceful warnings and continued operation when encountering such files

### Testing Status
- Basic functionality verified via manual testing
- Special character cases documented in TEST_CASE.md
- Automated test script created at test_special.sh
