# dataset-wrangler

Here’s a ready-to-run Python CLI script that renames all images in a folder with sequential numbering, supports a preview of the first rename, and interactively handles collisions.


Here’s a Python CLI script that splits all files in a source folder into train/val/test sets using a 70/20/10 ratio. It supports both copying (default) and moving, lets you set a random seed for reproducibility, and provides a preview mode.



Scans a directory for duplicate files (by SHA256) and corrupt images.
Removes duplicates (keeping one copy) and deletes unreadable image files.

Usage:
  python cleanup_dataset.py --dir /path/to/folder [--dry-run]
"""
