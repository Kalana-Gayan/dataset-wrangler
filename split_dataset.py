#!/usr/bin/env python3
"""
split_dataset.py

Splits files in a directory into train/val/test subdirectories
with a default 70/20/10 ratio.

Features:
- Configurable ratios and random seed
- Copy (default) or move mode
- --preview to show counts without touching any files
- Summary of successes and failures
"""

import argparse
import os
import random
import shutil
import sys

def parse_args():
    parser = argparse.ArgumentParser(
        description="Split a dataset folder into train/val/test (default 70/20/10)"
    )
    parser.add_argument(
        "-s", "--src-dir",
        required=True,
        help="Source directory containing your files"
    )
    parser.add_argument(
        "-d", "--dest-dir",
        default=".",
        help="Destination root directory (default: current folder)"
    )
    parser.add_argument(
        "--train-ratio",
        type=float,
        default=0.7,
        help="Proportion for training set (default: 0.7)"
    )
    parser.add_argument(
        "--val-ratio",
        type=float,
        default=0.2,
        help="Proportion for validation set (default: 0.2)"
    )
    parser.add_argument(
        "--test-ratio",
        type=float,
        default=0.1,
        help="Proportion for test set (default: 0.1)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for shuffling (default: 42)"
    )
    parser.add_argument(
        "--move",
        action="store_true",
        help="Move files instead of copying"
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Only print split counts; do not copy/move files"
    )
    return parser.parse_args()


def validate_ratios(train, val, test):
    total = train + val + test
    if not abs(total - 1.0) < 1e-6:
        sys.exit(f"Error: Ratios must sum to 1.0 (currently {total})")


def gather_files(src_dir):
    return sorted(
        f for f in os.listdir(src_dir)
        if os.path.isfile(os.path.join(src_dir, f))
    )


def make_dirs(root, subsets):
    for name in subsets:
        path = os.path.join(root, name)
        os.makedirs(path, exist_ok=True)


def split_indices(n, train_r, val_r):
    n_train = int(n * train_r)
    n_val = int(n * val_r)
    n_test = n - n_train - n_val
    return (
        list(range(0, n_train)),
        list(range(n_train, n_train + n_val)),
        list(range(n_train + n_val, n))
    )


def dispatch_file(src, dst, move_mode):
    if move_mode:
        return shutil.move(src, dst)
    else:
        return shutil.copy2(src, dst)


def main():
    args = parse_args()
    validate_ratios(args.train_ratio, args.val_ratio, args.test_ratio)

    files = gather_files(args.src_dir)
    if not files:
        sys.exit("No files found in source directory.")

    random.seed(args.seed)
    random.shuffle(files)

    train_idx, val_idx, test_idx = split_indices(
        len(files),
        args.train_ratio,
        args.val_ratio
    )

    subsets = {
        "train": [files[i] for i in train_idx],
        "val":   [files[i] for i in val_idx],
        "test":  [files[i] for i in test_idx],
    }

    print("Preview of split counts:")
    for name, lst in subsets.items():
        print(f"  {name}: {len(lst)} files")
    if args.preview:
        sys.exit(0)

    make_dirs(args.dest_dir, subsets.keys())

    moved = copied = errs = 0
    for subset_name, file_list in subsets.items():
        for filename in file_list:
            src_path = os.path.join(args.src_dir, filename)
            dst_path = os.path.join(args.dest_dir, subset_name, filename)
            try:
                dispatch_file(src_path, dst_path, args.move)
                if args.move:
                    moved += 1
                else:
                    copied += 1
            except Exception as e:
                print(f"[ERROR] {filename} → {subset_name}: {e}")
                errs += 1

    action = "Moved" if args.move else "Copied"
    print(f"\nDone. {action}: {moved if args.move else copied}, Errors: {errs}")


if __name__ == "__main__":
    main()
