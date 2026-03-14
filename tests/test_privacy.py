"""Tests for privacy detector."""
import os
import tempfile
from datavault.privacy import PrivacyDetector


def test_detect_email():
    d = PrivacyDetector()
    result = d.scan_text("Contact us at user@example.com for info.")
    assert result["has_sensitive"]
    assert result["findings"][0]["type"] == "email"
    assert result["findings"][0]["count"] == 1


def test_detect_phone_cn():
    d = PrivacyDetector()
    result = d.scan_text("Call me: 13812345678")
    assert result["has_sensitive"]
    types = [f["type"] for f in result["findings"]]
    assert "phone_cn" in types


def test_detect_id_card_cn():
    d = PrivacyDetector()
    result = d.scan_text("ID: 110101199001011234")
    assert result["has_sensitive"]
    types = [f["type"] for f in result["findings"]]
    assert "id_card_cn" in types


def test_detect_credit_card():
    d = PrivacyDetector()
    result = d.scan_text("Card: 4111 1111 1111 1111")
    assert result["has_sensitive"]
    types = [f["type"] for f in result["findings"]]
    assert "credit_card" in types


def test_detect_ip_address():
    d = PrivacyDetector()
    result = d.scan_text("Server at 192.168.1.100")
    assert result["has_sensitive"]
    types = [f["type"] for f in result["findings"]]
    assert "ip_address" in types


def test_detect_api_key():
    d = PrivacyDetector()
    result = d.scan_text("api_key='abcdefghij1234567890'")
    assert result["has_sensitive"]
    types = [f["type"] for f in result["findings"]]
    assert "api_key" in types


def test_no_sensitive():
    d = PrivacyDetector()
    result = d.scan_text("Hello world, nothing sensitive here.")
    assert not result["has_sensitive"]
    assert result["findings"] == []


def test_scan_file():
    d = PrivacyDetector()
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False
    ) as f:
        f.write("Email: test@example.com\nPhone: 13900001111\n")
        f.flush()
        result = d.scan_file(f.name)
        assert result["has_sensitive"]
        types = [item["type"] for item in result["findings"]]
        assert "email" in types
        assert "phone_cn" in types
        os.unlink(f.name)


def test_scan_binary_skip():
    d = PrivacyDetector()
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        f.write(b"\x89PNG\r\n test@example.com")
        f.flush()
        result = d.scan_file(f.name)
        assert not result["has_sensitive"]
        os.unlink(f.name)


def test_risk_level_safe():
    d = PrivacyDetector()
    findings = {"has_sensitive": False, "findings": []}
    assert d.risk_level(findings) == "safe"


def test_risk_level_low():
    d = PrivacyDetector()
    findings = {"has_sensitive": True, "findings": [{"type": "email", "count": 1, "sample": "a@b.com"}]}
    assert d.risk_level(findings) == "low"


def test_risk_level_medium():
    d = PrivacyDetector()
    findings = {"has_sensitive": True, "findings": [{"type": "id_card_cn", "count": 1, "sample": "x"}]}
    assert d.risk_level(findings) == "medium"


def test_risk_level_high():
    d = PrivacyDetector()
    findings = {"has_sensitive": True, "findings": [
        {"type": "id_card_cn", "count": 2, "sample": "x"},
        {"type": "email", "count": 3, "sample": "a@b.com"},
    ]}
    assert d.risk_level(findings) == "high"


def test_risk_level_critical():
    d = PrivacyDetector()
    findings = {"has_sensitive": True, "findings": [
        {"type": "id_card_cn", "count": 5, "sample": "x"},
    ]}
    assert d.risk_level(findings) == "critical"


def test_multiple_patterns():
    d = PrivacyDetector()
    text = "Email: a@b.com, Card: 4111 1111 1111 1111, IP: 10.0.0.1"
    result = d.scan_text(text)
    assert result["has_sensitive"]
    types = {f["type"] for f in result["findings"]}
    assert "email" in types
    assert "credit_card" in types
    assert "ip_address" in types
