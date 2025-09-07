#!/usr/bin/env python3
"""
batch_rename_images.py

Renames images in a folder with sequential numbering:
  img_001.jpg, img_002.png, etc.

Features:
- Configurable prefix, start index, zero-padding, and extensions
- --preview mode shows the first mapping without renaming
- Interactive collision handling: overwrite / skip / auto-rename
- Error logging to console
"""

import argparse
import os
import sys
from datetime import datetime

# Configuration defaults (can be overridden via CLI)
PREFIX = "img"
START_INDEX = 1
NUM_DIGITS = 3
EXTENSIONS = ("jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Batch rename images with sequential numbering"
    )
    parser.add_argument(
        "-d", "--dir",
        default=".",
        help="Target directory (default: current folder)"
    )
    parser.add_argument(
        "-p", "--prefix",
        default=PREFIX,
        help=f"Filename prefix (default: '{PREFIX}')"
    )
    parser.add_argument(
        "-s", "--start",
        type=int,
        default=START_INDEX,
        help=f"Starting index (default: {START_INDEX})"
    )
    parser.add_argument(
        "-n", "--digits",
        type=int,
        default=NUM_DIGITS,
        help=f"Number of digits for zero-padding (default: {NUM_DIGITS})"
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Show mapping for the first file, then exit"
    )
    return parser.parse_args()


def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")


def ask_collision_action(old, new):
    prompt = f"Target exists: '{new}'. [O]verwrite / [S]kip / [R]ename? "
    while True:
        choice = input(prompt).strip().lower()
        if choice in ("o", "overwrite"):
            return "overwrite"
        if choice in ("s", "skip"):
            return "skip"
        if choice in ("r", "rename"):
            return "rename"
        print("Enter O, S, or R.")


def resolve_collision(target_path):
    base, ext = os.path.splitext(target_path)
    idx = 1
    while True:
        new_path = f"{base}_{idx}{ext}"
        if not os.path.exists(new_path):
            return new_path
        idx += 1


def main():
    args = parse_args()

    # Gather files
    all_files = sorted(os.listdir(args.dir))
    images = [
        f for f in all_files
        if os.path.isfile(os.path.join(args.dir, f))
        and f.lower().split(".")[-1] in EXTENSIONS
    ]

    if not images:
        log("No image files found. Exiting.")
        sys.exit(0)

    index = args.start
    renamed_count = 0
    skipped_count = 0
    error_count = 0

    for i, filename in enumerate(images):
        ext = filename.lower().split(".")[-1]
        new_name = f"{args.prefix}_{str(index).zfill(args.digits)}.{ext}"
        old_path = os.path.join(args.dir, filename)
        new_path = os.path.join(args.dir, new_name)

        # Preview mode: show first mapping, then exit
        if args.preview:
            log(f"Preview: '{filename}' → '{new_name}'")
            sys.exit(0)

        # Handle collision
        if os.path.exists(new_path):
            action = ask_collision_action(old_path, new_path)
            if action == "skip":
                log(f"Skipping '{filename}'")
                skipped_count += 1
                index += 1
                continue
            if action == "rename":
                resolved = resolve_collision(new_path)
                log(f"Auto-renamed collision to '{os.path.basename(resolved)}'")
                new_path = resolved
            # if overwrite, fall through to rename

        # Perform rename
        try:
            os.replace(old_path, new_path)
            log(f"Renamed '{filename}' → '{os.path.basename(new_path)}'")
            renamed_count += 1
        except Exception as e:
            log(f"Error renaming '{filename}': {e}")
            error_count += 1

        index += 1

    # Summary
    log(f"Done. Renamed: {renamed_count}, Skipped: {skipped_count}, Errors: {error_count}")


if __name__ == "__main__":
    main()
