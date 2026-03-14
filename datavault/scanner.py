"""Recursive directory scanner with file classification."""
import hashlib
import os
from typing import Any, Dict, Optional

from datavault.classifier import classify_path


def _sha256(path: str) -> str:
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def scan_directory(
    path: str,
    recursive: bool = True,
    skip_privacy: bool = False,
    save: bool = False,
    inventory: Optional[Any] = None,
) -> Dict[str, Any]:
    """Scan a directory and return categorized file counts and details."""
    from datavault.privacy import PrivacyDetector

    detector = None if skip_privacy else PrivacyDetector()
    categories: Dict[str, int] = {}
    risk_summary: Dict[str, int] = {}
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
                info["path"] = fpath
                info["hash"] = _sha256(fpath)

                # Privacy detection
                if detector is not None:
                    findings = detector.scan_file(fpath)
                    risk = detector.risk_level(findings)
                    info["privacy_risk"] = risk
                    info["privacy_findings"] = findings
                else:
                    info["privacy_risk"] = "safe"
                    info["privacy_findings"] = {"has_sensitive": False, "findings": []}

                risk_summary[info["privacy_risk"]] = (
                    risk_summary.get(info["privacy_risk"], 0) + 1
                )

                cat = info["category"]
                categories[cat] = categories.get(cat, 0) + 1
                files.append(info)

                # Save to inventory
                if save and inventory is not None:
                    inventory.upsert(info)

            except Exception:
                errors += 1

        if not recursive:
            break

    return {
        "root": os.path.abspath(path),
        "total": total,
        "errors": errors,
        "categories": categories,
        "risk_summary": risk_summary,
        "files": files,
    }
