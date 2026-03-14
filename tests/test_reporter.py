"""Tests for report generation."""
from datavault.reporter import generate_report


def _make_scan_result():
    return {
        "root": "/tmp/test",
        "total": 3,
        "errors": 0,
        "categories": {"code": 2, "image": 1},
        "risk_summary": {"safe": 2, "high": 1},
        "files": [
            {"path": "/tmp/test/a.py", "category": "code", "size": 100, "privacy_risk": "safe"},
            {"path": "/tmp/test/b.py", "category": "code", "size": 200, "privacy_risk": "high"},
            {"path": "/tmp/test/c.jpg", "category": "image", "size": 5000, "privacy_risk": "safe"},
        ],
    }


def test_text_report():
    report = generate_report(_make_scan_result(), fmt="text")
    assert "DataVault Report" in report
    assert "Total files: 3" in report
    assert "code" in report
    assert "image" in report
    assert "Privacy Risks:" in report
    assert "high" in report


def test_text_report_no_risk():
    result = _make_scan_result()
    result["risk_summary"] = {"safe": 3}
    report = generate_report(result, fmt="text")
    assert "Privacy Risks:" not in report


def test_json_report():
    import json
    report = generate_report(_make_scan_result(), fmt="json")
    data = json.loads(report)
    assert data["total_files"] == 3
    assert data["categories"]["code"] == 2
    assert data["risk_summary"]["high"] == 1


def test_markdown_report():
    report = generate_report(_make_scan_result(), fmt="markdown")
    assert "# DataVault Report" in report
    assert "| Category |" in report
    assert "## Privacy Risks" in report
    assert "**high**" in report


def test_markdown_report_no_risk():
    result = _make_scan_result()
    result["risk_summary"] = {"safe": 3}
    report = generate_report(result, fmt="markdown")
    assert "## Privacy Risks" not in report
