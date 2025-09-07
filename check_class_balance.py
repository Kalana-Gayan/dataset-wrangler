#!/usr/bin/env python3
"""
check_class_balance.py

Scans a dataset organized by class subdirectories, counts samples per class,
and warns if any class is underrepresented based on ratio or absolute difference.

Usage:
  python check_class_balance.py --dir /path/to/dataset [options]

Features:
- Assumes each class is a subdirectory under the target directory.
- Counts files with configurable extensions.
- Alerts if any class count / max_count < ratio_threshold.
- Alerts if max_count – class_count > diff_threshold.
- Prints a summary table of counts.
"""

import argparse
import os
import sys
from tabulate import tabulate

# Supported file extensions
EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp")

def parse_args():
    parser = argparse.ArgumentParser(
        description="Check class balance in a dataset directory"
    )
    parser.add_argument(
        "-d", "--dir",
        default=".",
        help="Root directory of dataset (each subfolder is a class)"
    )
    parser.add_argument(
        "--ratio-threshold",
        type=float,
        default=0.5,
        help="Warn if class_count / max_count < this ratio (default: 0.5)"
    )
    parser.add_argument(
        "--diff-threshold",
        type=int,
        default=50,
        help="Warn if max_count - class_count > this absolute difference (default: 50)"
    )
    return parser.parse_args()

def gather_class_counts(root_dir):
    counts = {}
    for entry in os.listdir(root_dir):
        class_path = os.path.join(root_dir, entry)
        if os.path.isdir(class_path):
            files = [
                f for f in os.listdir(class_path)
                if os.path.isfile(os.path.join(class_path, f))
                and os.path.splitext(f)[1].lower() in EXTENSIONS
            ]
            counts[entry] = len(files)
    return counts

def main():
    args = parse_args()
    root = args.dir

    if not os.path.isdir(root):
        sys.exit(f"Error: '{root}' is not a directory.")

    counts = gather_class_counts(root)
    if not counts:
        sys.exit("No class subdirectories with supported files found.")

    # Compute metrics
    max_count = max(counts.values())
    summary = []
    imbalance = False

    for cls, cnt in sorted(counts.items()):
        ratio = cnt / max_count
        diff = max_count - cnt
        warn_ratio = ratio < args.ratio_threshold
        warn_diff  = diff > args.diff_threshold
        status = []
        if warn_ratio:
            status.append(f"ratio<{args.ratio_threshold:.2f}")
        if warn_diff:
            status.append(f"diff>{args.diff_threshold}")
        summary.append([cls, cnt, f"{ratio:.2f}", diff, "; ".join(status) or "OK"])
        if status:
            imbalance = True

    # Print table
    print(tabulate(
        summary,
        headers=["Class", "Count", "Count/Max", "Diff", "Status"],
        tablefmt="github"
    ))

    if imbalance:
        print("\nWARNING: Class imbalance detected.")
        sys.exit(1)
    else:
        print("\nAll classes are balanced within thresholds.")
        sys.exit(0)

if __name__ == "__main__":
    main()
