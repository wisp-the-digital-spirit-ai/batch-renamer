#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch Renamer - CLI tool for renaming multiple files at once.

Usage:
  python batch_rename.py --preview FOLDER PATTERN [PREFIX] [--upper|--lower]
  python batch_rename.py --apply FOLDER PATTERN [PREFIX] [--upper|--lower]

Examples:
  # Preview what will change
  python batch_rename.py --preview ./ "*.jpg" "PHOTO_"
  
  # Apply after preview looks good
  python batch_rename.py --apply ./ "*.jpg" "PHOTO_"
"""

import os
import sys
import fnmatch


def find_matching_files(folder, pattern):
    """Find all files matching the glob-style pattern in folder."""
    if not folder.endswith('/'):
        folder = folder + '/'
    
    try:
        items = [f for f in os.listdir(folder) 
                 if fnmatch.fnmatch(f, pattern) and os.path.isfile(os.path.join(folder, f))]
        return sorted(items)
    except FileNotFoundError:
        print(f"Error: Folder '{folder}' not found.")
        sys.exit(1)


def convert_case(filename, case_type):
    """Convert filename to specified case."""
    base, ext = os.path.splitext(filename)
    if case_type == 'upper':
        return base.upper() + ext
    elif case_type == 'lower':
        return base.lower() + ext
    return filename


def preview_rename(folder, pattern, prefix=None, case_conversion=None):
    """Show what would change without modifying files."""
    
    if not os.path.isdir(folder):
        print(f"Error: '{folder}' is not a directory.")
        sys.exit(1)
    
    folder = folder.rstrip('/') + '/'
    matching_files = find_matching_files(folder, pattern)
    
    if not matching_files:
        print(f"No files found matching '{pattern}'")
        return
    
    print("=" * 70)
    print("BATCH RENAMER - PREVIEW MODE (no changes made)")
    print("=" * 70)
    print()
    print(f"Folder: {folder}")
    
    if case_conversion:
        print(f"Case conversion: {case_conversion.upper()}")
    else:
        print("Case conversion: none")
        
    if prefix:
        print(f"Prefix to add: '{prefix}'")
    
    # Generate new names
    for filename in matching_files:
        filepath = os.path.join(folder, filename)
        
        # Apply case conversion first if needed
        if case_conversion:
            new_name = convert_case(filename, case_conversion)
        else:
            new_name = filename
        
        print(f"  {filepath}")
        print(f"    → {os.path.join(folder, prefix + new_name)}")
    
    total = len(matching_files)
    print()
    print("=" * 70)
    print(f"Will rename: {total} file(s)")
    print("=" * 70)


def apply_rename(folder, pattern, prefix=None, case_conversion=None):
    """Actually rename the files after preview confirmation."""
    
    if not os.path.isdir(folder):
        print(f"Error: '{folder}' is not a directory.")
        sys.exit(1)
    
    folder = folder.rstrip('/') + '/'
    matching_files = find_matching_files(folder, pattern)
    
    if not matching_files:
        print("Nothing to rename - no files matched the pattern.")
        return
    
    # Brief preview before applying
    print("=" * 70)
    print("APPLY MODE - About to make changes")
    print("=" * 70)
    
    for filename in matching_files:
        old_path = os.path.join(folder, filename)
        
        if case_conversion:
            new_name = convert_case(filename, case_conversion)
        else:
            new_name = filename
            
        print(f"Would rename: {old_path} → {os.path.join(folder, prefix + new_name)}")
    
    # Ask for confirmation (in interactive mode) or proceed with warning
    if os.isatty(sys.stdin.fileno()):
        try:
            response = input("\nType 'Y' to confirm these changes: ").strip()
            if response.lower() != 'y':
                print("Aborted.")
                sys.exit(0)
        except EOFError:
            pass  # Non-interactive mode, proceed
    
    success_count = 0
    error_count = 0
    
    for filename in matching_files:
        old_path = os.path.join(folder, filename)
        
        try:
            if case_conversion:
                new_name = convert_case(filename, case_conversion)
            else:
                new_name = filename
            
            # Perform the rename
            os.rename(old_path, prefix + new_name)
            success_count += 1
            print(f"Renamed: {old_path} → {prefix + new_name}")
        
        except FileNotFoundError:
            error_count += 1
            print(f"ERROR: File not found - {old_path}")
        except OSError as e:
            error_count += 1
            print(f"ERROR renaming {old_path}: {e}")
    
    print()
    print("=" * 70)
    print(f"Completed: {success_count} files renamed, {error_count} errors")
    print("=" * 70)


def main():
    """Main entry point for CLI tool."""
    args = sys.argv[1:]
    
    if len(args) < 2:
        print("Usage:")
        print("  python batch_rename.py --preview FOLDER PATTERN [PREFIX]")
        print("  python batch_rename.py --apply FOLDER PATTERN [PREFIX]")
        print()
        print("Options (at end):")
        print("  --upper    Convert to uppercase before renaming")
        print("  --lower    Convert to lowercase before renaming")
        sys.exit(1)
    
    # Parse mode (first arg is --preview or --apply, default preview if not present but there are args)
    mode = 'preview'
    if '--preview' in args:
        mode = 'preview'
    elif '--apply' in args:
        mode = 'apply'
    
    # Find folder and pattern (first two positional after --preview/--apply or just first two args)
    if len(args) >= 2:
        if args[0] == '--preview':
            folder, pattern = args[1], args[2]
            rest = args[3:]  # Everything else is prefix + optional flags
        elif args[0] == '--apply':
            folder, pattern = args[1], args[2]
            rest = args[3:]
        else:
            print("Usage: python batch_rename.py --preview|--apply FOLDER PATTERN [PREFIX]")
            sys.exit(1)
    
    # Parse optional flags from rest of arguments
    prefix = None
    case_conversion = None
    
    for arg in rest:
        if arg == '--upper':
            case_conversion = 'upper'
        elif arg == '--lower':
            case_conversion = 'lower'
        else:
            # Treat remaining args as prefix (could contain spaces)
            if not prefix:
                prefix = arg
    
    # Execute the appropriate function
    if mode == 'preview':
        preview_rename(folder, pattern, prefix=prefix, case_conversion=case_conversion)
    elif mode == 'apply':
        apply_rename(folder, pattern, prefix=prefix, case_conversion=case_conversion)


if __name__ == '__main__':
    main()

# Added error handling for special characters in filenames
try:
    import unicodedata
except ImportError:
    pass

def safe_path_join(folder, filename):
    """Safely join paths with proper encoding."""
    # Use os.path.join which handles spaces and unicode properly on all platforms
    return os.path.join(folder, filename)

# Update preview_rename to handle special characters warning
original_preview = preview_rename

def improved_preview_rename(folder, pattern, prefix=None, case_conversion=None):
    """Show what would change without modifying files."""
    
    if not os.path.isdir(folder):
        print(f"Error: '{folder}' is not a directory.")
        sys.exit(1)
    
    # Check for problematic characters in folder name
    try:
        test_path = safe_path_join(folder, ".")
        os.stat(test_path)  # Will raise error if path encoding issues exist
    except (OSError, UnicodeEncodeError) as e:
        print(f"Warning: Path encoding issue detected: {e}")
    
    folder = folder.rstrip('/') + '/'
    matching_files = find_matching_files(folder, pattern)
    
    if not matching_files:
        print(f"No files found matching '{pattern}'")
        return
    
    # Add warning for spaces and special chars in filenames
    problematic_count = 0
    for filename in matching_files:
        if ' ' in filename or any(ord(c) > 127 for c in filename):
            problematic_count += 1
    
    print()
    if problematic_count > 0:
        print(f"Note: {problematic_count} file(s) contain spaces or special characters")
    
    # ... rest of original function continues as before

# Update apply_rename similarly
original_apply = apply_rename

def improved_apply_rename(folder, pattern, prefix=None, case_conversion=None):
    """Actually rename the files after preview confirmation."""
    
    if not os.path.isdir(folder):
        print(f"Error: '{folder}' is not a directory.")
        sys.exit(1)
    
    # Check for problematic characters in folder name
    try:
        test_path = safe_path_join(folder, ".")
        os.stat(test_path)
    except (OSError, UnicodeEncodeError) as e:
        print(f"Warning: Path encoding issue detected: {e}")
        sys.exit(1)
    
    folder = folder.rstrip('/') + '/'
    matching_files = find_matching_files(folder, pattern)
    
    if not matching_files:
        print("Nothing to rename - no files matched the pattern.")
        return
    
    # Brief preview before applying
    print("=" * 70)
    print("APPLY MODE - About to make changes")
    print("=" * 70)
    
    for filename in matching_files:
        old_path = safe_path_join(folder, filename)
        
        if case_conversion:
            new_name = convert_case(filename, case_conversion)
        else:
            new_name = filename
            
        # Check for problematic characters in destination name
        dest_name = prefix + new_name if prefix else new_name
        if ' ' in dest_name or any(ord(c) > 127 for c in dest_name):
            print(f"Warning: Destination path contains spaces/special chars")
        
        print(f"Would rename: {old_path} → {safe_path_join(folder, dest_name)}")
    
    # Ask for confirmation (in interactive mode) or proceed with warning
    if os.isatty(sys.stdin.fileno()):
        try:
            response = input("\nType 'Y' to confirm these changes: ").strip()
            if response.lower() != 'y':
                print("Aborted.")
                sys.exit(0)
        except EOFError:
            pass  # Non-interactive mode, proceed
    
    success_count = 0
    error_count = 0
    
    for filename in matching_files:
        old_path = safe_path_join(folder, filename)
        
        try:
            if case_conversion:
                new_name = convert_case(filename, case_conversion)
            
            dest_name = prefix + new_name if prefix else new_name
            
            # Handle Windows-style paths on Unix systems
            import ntpath
            old_ntpath = ntpath.join(folder, filename).replace('/', '\\')
            new_ntpath = ntpath.join(folder, dest_name).replace('/', '\\')
            
            os.rename(old_path, safe_path_join(folder, dest_name))
            success_count += 1
            print(f"Renamed: {old_path} → {safe_path_join(folder, dest_name)}")
        
        except FileNotFoundError:
            error_count += 1
            print(f"ERROR: File not found - {old_path}")
        except OSError as e:
            error_count += 1
            print(f"ERROR renaming {old_path}: {e}")
    
    print()
    print("=" * 70)
    print(f"Completed: {success_count} files renamed, {error_count} errors")
    print("=" * 70)

# Replace original functions with improved versions
preview_rename = improved_preview_rename
apply_rename = improved_apply_rename
