#!/usr/bin/env python3
"""
cleanup_dataset.py

Scans a directory for duplicate files (by SHA256) and corrupt images.
Removes duplicates (keeping one copy) and deletes unreadable image files.

Usage:
  python cleanup_dataset.py --dir /path/to/folder [--dry-run]
"""

import argparse
import hashlib
import os
import sys
from PIL import Image, UnidentifiedImageError

# Supported image extensions
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp")

def parse_args():
    parser = argparse.ArgumentParser(
        description="Remove duplicate files and corrupt images from a folder"
    )
    parser.add_argument(
        "-d", "--dir",
        default=".",
        help="Target directory (default: current folder)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deleted without actually removing files"
    )
    return parser.parse_args()

def compute_hash(path, block_size=65536):
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            hasher.update(block)
    return hasher.hexdigest()

def find_duplicates(file_paths):
    hashes = {}
    duplicates = []
    for path in file_paths:
        file_hash = compute_hash(path)
        if file_hash in hashes:
            duplicates.append((path, hashes[file_hash]))
        else:
            hashes[file_hash] = path
    return duplicates

def is_corrupt_image(path):
    try:
        with Image.open(path) as img:
            img.verify()
        return False
    except (UnidentifiedImageError, OSError):
        return True

def gather_all_files(root_dir):
    all_files = []
    for fname in os.listdir(root_dir):
        full = os.path.join(root_dir, fname)
        if os.path.isfile(full):
            all_files.append(full)
    return sorted(all_files)

def main():
    args = parse_args()
    root = args.dir

    if not os.path.isdir(root):
        print(f"Error: '{root}' is not a directory.")
        sys.exit(1)

    files = gather_all_files(root)

    # Detect duplicates
    duplicates = find_duplicates(files)
    # Detect corrupt images
    corrupts = [
        path for path in files
        if os.path.splitext(path)[1].lower() in IMAGE_EXTENSIONS
        and is_corrupt_image(path)
    ]

    if not duplicates and not corrupts:
        print("No duplicates or corrupt images found.")
        return

    # Summarize
    print("Summary:")
    if duplicates:
        print(f"  Duplicates (will remove one of each pair): {len(duplicates)} files")
    if corrupts:
        print(f"  Corrupt images (will remove): {len(corrupts)} files")
    if args.dry_run:
        print("\nDry-run mode enabled. No files will be deleted.")
    print()

    # Process duplicates
    for dup_path, orig_path in duplicates:
        print(f"[DUP] Remove: {dup_path}  (duplicate of {orig_path})")
        if not args.dry_run:
            try:
                os.remove(dup_path)
            except Exception as e:
                print(f"  [ERROR] Failed to delete {dup_path}: {e}")

    # Process corrupt images
    for corrupt_path in corrupts:
        print(f"[CORRUPT] Remove: {corrupt_path}")
        if not args.dry_run:
            try:
                os.remove(corrupt_path)
            except Exception as e:
                print(f"  [ERROR] Failed to delete {corrupt_path}: {e}")

    if not args.dry_run:
        print("\nCleanup complete.")

if __name__ == "__main__":
    main()
