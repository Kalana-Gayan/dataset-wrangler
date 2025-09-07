# ⚡dataset-wrangler
---
## 📌 batch_rename_images.py
Here’s a ready-to-run Python CLI script that renames all images in a folder with sequential numbering, supports a preview of the first rename, and interactively handles collisions.

**Renames images in a folder with sequential numbering:**
  img_001.jpg, img_002.png, etc.

**Features:**
- Configurable prefix, start index, zero-padding, and extensions
- --preview mode shows the first mapping without renaming
- Interactive collision handling: overwrite / skip / auto-rename
- Error logging to console
**Usage**
  `python3 batch_rename_images.py -d demo `
---
## 🌁split_dataset.py
Here’s a Python CLI script that splits all files in a source folder into train/val/test sets using a 70/20/10 ratio. It supports both copying (default) and moving, lets you set a random seed for reproducibility, and provides a preview mode.

Splits files in a directory into train/val/test subdirectories with a default 70/20/10 ratio.

**Features:**
- Configurable ratios and random seed
- Copy (default) or move mode
- --preview to show counts without touching any files
- Summary of successes and failures
---
## 🏮cleanup_dataset.py
Scans a directory for duplicate files (by SHA256) and corrupt images. Removes duplicates (keeping one copy) and deletes unreadable image files.

**Usage:**
  `python cleanup_dataset.py --dir /path/to/folder [--dry-run]`

---
## 📍check_class_balance.py
Scans a dataset organized by class subdirectories, counts samples per class,and warns if any class is underrepresented based on ratio or absolute difference.
dataset/

**Assume your folder structure is:**
```
├── cat/
│   ├── img1.jpg
│   └── img2.png
└── dog/
    ├── dog_a.jpg
    ├── dog_b.jpg
    └── dog_c.png
```

**Usage:**
  python check_class_balance.py --dir /path/to/dataset [options]

**Features:**
- Assumes each class is a subdirectory under the target directory.
- Counts files with configurable extensions.
- Alerts if any class count / max_count < ratio_threshold.
- Alerts if max_count – class_count > diff_threshold.
- Prints a summary table of counts.
