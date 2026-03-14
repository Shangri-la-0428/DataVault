"""Report generation from scan results."""
import json
from typing import Any, Dict


def _human_size(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(n) < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024  # type: ignore
    return f"{n:.1f} PB"


_RISK_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "safe": 4}


def generate_report(scan_result: Dict[str, Any], fmt: str = "text") -> str:
    if fmt == "json":
        summary = {
            "root": scan_result["root"],
            "total_files": scan_result["total"],
            "categories": scan_result["categories"],
            "total_size": sum(f["size"] for f in scan_result["files"]),
            "risk_summary": scan_result.get("risk_summary", {}),
        }
        return json.dumps(summary, indent=2, ensure_ascii=False)

    if fmt == "markdown":
        return _markdown_report(scan_result)

    return _text_report(scan_result)


def _text_report(scan_result: Dict[str, Any]) -> str:
    lines = [
        "DataVault Report",
        "=" * 40,
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

    # Privacy risk summary
    risk_summary = scan_result.get("risk_summary", {})
    if risk_summary and set(risk_summary.keys()) != {"safe"}:
        lines.append("")
        lines.append("Privacy Risks:")
        for risk, count in sorted(
            risk_summary.items(), key=lambda x: _RISK_ORDER.get(x[0], 9)
        ):
            if risk != "safe":
                lines.append(f"  {risk:15s}  {count:5d} files")

    lines.append(f"\nTotal size: {_human_size(total_size)}")
    return "\n".join(lines)


def _markdown_report(scan_result: Dict[str, Any]) -> str:
    lines = [
        "# DataVault Report",
        "",
        f"**Root:** `{scan_result['root']}`  ",
        f"**Total files:** {scan_result['total']}  ",
        f"**Errors:** {scan_result['errors']}",
        "",
        "## Categories",
        "",
        "| Category | Files | Size |",
        "|----------|------:|-----:|",
    ]
    total_size = 0
    for cat, count in sorted(scan_result["categories"].items(), key=lambda x: -x[1]):
        cat_size = sum(f["size"] for f in scan_result["files"] if f["category"] == cat)
        total_size += cat_size
        lines.append(f"| {cat} | {count} | {_human_size(cat_size)} |")

    # Privacy risk summary
    risk_summary = scan_result.get("risk_summary", {})
    if risk_summary and set(risk_summary.keys()) != {"safe"}:
        lines.append("")
        lines.append("## Privacy Risks")
        lines.append("")
        lines.append("| Risk Level | Files |")
        lines.append("|------------|------:|")
        for risk, count in sorted(
            risk_summary.items(), key=lambda x: _RISK_ORDER.get(x[0], 9)
        ):
            if risk != "safe":
                lines.append(f"| **{risk}** | {count} |")

    lines.append(f"\n**Total size:** {_human_size(total_size)}")
    return "\n".join(lines)
