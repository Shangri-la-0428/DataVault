"""Privacy detector — scan files and text for sensitive information."""
import os
import re
from typing import Dict, List, Any


class PrivacyDetector:
    """Detect sensitive information in files and text."""

    PATTERNS = {
        "email": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
        "phone_cn": re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"),
        "id_card_cn": re.compile(r"(?<!\d)\d{17}[\dXx](?!\d)"),
        "credit_card": re.compile(r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b"),
        "ip_address": re.compile(
            r"\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
            r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b"
        ),
        "api_key": re.compile(
            r"""(?:api[_-]?key|token|secret)[=:]\s*["']\w{16,}["']""", re.IGNORECASE
        ),
    }

    # Risk weights per pattern type
    _WEIGHTS: Dict[str, int] = {
        "email": 1,
        "phone_cn": 2,
        "id_card_cn": 4,
        "credit_card": 4,
        "ip_address": 1,
        "api_key": 3,
    }

    # Max bytes to read from a single file (16 MB)
    MAX_FILE_SIZE = 16 * 1024 * 1024

    # Extensions we should skip (binary files unlikely to have readable PII)
    _BINARY_EXTS = frozenset({
        ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".webp", ".tiff",
        ".heic", ".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a",
        ".mp4", ".mkv", ".avi", ".mov", ".webm",
        ".zip", ".tar", ".gz", ".bz2", ".7z", ".rar",
        ".exe", ".dll", ".so", ".dylib", ".pyc", ".pyo",
        ".db", ".sqlite", ".sqlite3",
    })

    def scan_text(self, text: str) -> Dict[str, Any]:
        """Scan text content and return findings."""
        findings: List[Dict[str, Any]] = []
        for name, pattern in self.PATTERNS.items():
            matches = pattern.findall(text)
            if matches:
                findings.append({
                    "type": name,
                    "count": len(matches),
                    "sample": matches[0],
                })
        return {
            "has_sensitive": len(findings) > 0,
            "findings": findings,
        }

    def scan_file(self, path: str) -> Dict[str, Any]:
        """Scan a file and return findings."""
        ext = os.path.splitext(path)[1].lower()
        if ext in self._BINARY_EXTS:
            return {"has_sensitive": False, "findings": []}

        try:
            size = os.path.getsize(path)
            if size > self.MAX_FILE_SIZE:
                return {"has_sensitive": False, "findings": []}
            with open(path, "r", errors="ignore") as f:
                text = f.read()
        except (OSError, UnicodeDecodeError):
            return {"has_sensitive": False, "findings": []}

        return self.scan_text(text)

    def risk_level(self, findings: Dict[str, Any]) -> str:
        """Assess risk level from findings: safe/low/medium/high/critical."""
        if not findings.get("has_sensitive"):
            return "safe"
        score = 0
        for item in findings["findings"]:
            weight = self._WEIGHTS.get(item["type"], 1)
            score += weight * item["count"]
        if score >= 20:
            return "critical"
        if score >= 10:
            return "high"
        if score >= 4:
            return "medium"
        return "low"
