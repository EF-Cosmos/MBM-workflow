#!/usr/bin/env python3
"""Package MBM_workflow addon into a distributable zip for Blender 5.0+."""

import argparse
import os
import re
import zipfile
from pathlib import Path

ADDON_ID = "MBM_workflow"

# Root-level files to include
INCLUDE_FILES = [
    "__init__.py",
    "load_modules.py",
    "config.py",
    "blender_manifest.toml",
    "ui.py",
    "ui_panels.py",
    "ui_dialogs.py",
    "ui_lists.py",
    "LICENSE",
    "README.md",
]

# Directories to include (recursive)
INCLUDE_DIRS = [
    "codes",
    "wheels",
    "i18n",
    "colors",
    "mutf8",
    "multiprocess",
]

# Subdirectory paths to exclude (relative to repo root, forward-slash)
EXCLUDE_SUBDIRS = {
    "codes/unuse",
}


def should_exclude(rel_path: str) -> bool:
    """Check if a relative path should be excluded from the package."""
    parts = Path(rel_path).parts
    if "__pycache__" in parts:
        return True
    for exc in EXCLUDE_SUBDIRS:
        if rel_path == exc or rel_path.startswith(exc + "/"):
            return True
    if rel_path.endswith((".pyc", ".pyo")):
        return True
    return False


def get_version(repo_root: Path) -> str:
    """Extract version from blender_manifest.toml."""
    manifest = repo_root / "blender_manifest.toml"
    content = manifest.read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
    if match:
        return match.group(1)
    raise ValueError("Could not find version in blender_manifest.toml")


def create_package(repo_root: Path, output_dir: Path, version: str | None = None) -> Path:
    """Create the release zip and return its path."""
    if version is None:
        version = get_version(repo_root)

    zip_name = f"{ADDON_ID}-{version}.zip"
    zip_path = output_dir / zip_name

    file_count = 0
    total_bytes = 0

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add root-level files
        for fname in INCLUDE_FILES:
            fpath = repo_root / fname
            if not fpath.exists():
                print(f"  WARNING: {fname} not found, skipping")
                continue
            zf.write(fpath, f"{ADDON_ID}/{fname}")
            file_count += 1
            total_bytes += fpath.stat().st_size

        # Add directories
        for dname in INCLUDE_DIRS:
            dpath = repo_root / dname
            if not dpath.exists():
                print(f"  WARNING: {dname}/ not found, skipping")
                continue
            for fpath in dpath.rglob("*"):
                if not fpath.is_file():
                    continue
                rel = fpath.relative_to(repo_root).as_posix()
                if should_exclude(rel):
                    continue
                zf.write(fpath, f"{ADDON_ID}/{rel}")
                file_count += 1
                total_bytes += fpath.stat().st_size

    zip_size = zip_path.stat().st_size
    print(f"Files: {file_count}")
    print(f"Uncompressed: {total_bytes:,} bytes ({total_bytes / 1024 / 1024:.1f} MB)")
    print(f"Zip size: {zip_size:,} bytes ({zip_size / 1024 / 1024:.1f} MB)")
    print(f"Output: {zip_path}")
    return zip_path


def main():
    parser = argparse.ArgumentParser(description="Package MBM_workflow for release")
    parser.add_argument("--version", help="Override version (default: from blender_manifest.toml)")
    parser.add_argument("--output-dir", default="dist", help="Output directory (default: dist)")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    create_package(repo_root, output_dir, args.version)


if __name__ == "__main__":
    main()
