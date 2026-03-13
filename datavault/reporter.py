"""Report generation from scan results."""
import json
from typing import Dict, Any


def _human_size(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(n) < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024  # type: ignore
    return f"{n:.1f} PB"


def generate_report(scan_result: Dict[str, Any], fmt: str = "text") -> str:
    if fmt == "json":
        summary = {
            "root": scan_result["root"],
            "total_files": scan_result["total"],
            "categories": scan_result["categories"],
            "total_size": sum(f["size"] for f in scan_result["files"]),
        }
        return json.dumps(summary, indent=2, ensure_ascii=False)

    lines = [
        f"DataVault Report",
        f"{'=' * 40}",
        f"Root: {scan_result['root']}",
        f"Total files: {scan_result['total']}",
        f"Errors: {scan_result['errors']}",
        "",
        "Categories:",
    ]
    total_size = 0
    for cat, count in sorted(scan_result["categories"].items(), key=lambda x: -x[1]):
        cat_size = sum(f["size"] for f in scan_result["files"] if f["category"] == cat)
        total_size += cat_size
        lines.append(f"  {cat:15s}  {count:5d} files  {_human_size(cat_size):>10s}")

    lines.append(f"\nTotal size: {_human_size(total_size)}")
    return "\n".join(lines)
