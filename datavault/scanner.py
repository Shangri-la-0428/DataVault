"""Recursive directory scanner with file classification."""
import os
from typing import Dict, Any
from datavault.classifier import classify_path


def scan_directory(path: str, recursive: bool = True) -> Dict[str, Any]:
    """Scan a directory and return categorized file counts and details."""
    categories: Dict[str, int] = {}
    files = []
    total = 0
    errors = 0

    for root, dirs, filenames in os.walk(path):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith(".")]

        for fname in filenames:
            if fname.startswith("."):
                continue
            fpath = os.path.join(root, fname)
            total += 1
            try:
                info = classify_path(fpath)
                cat = info["category"]
                categories[cat] = categories.get(cat, 0) + 1
                files.append({"path": fpath, **info})
            except Exception:
                errors += 1

        if not recursive:
            break

    return {
        "root": os.path.abspath(path),
        "total": total,
        "errors": errors,
        "categories": categories,
        "files": files,
    }
