"""Tests for SQLite inventory."""
import os
import tempfile
from datavault.inventory import Inventory


def _make_inventory():
    """Create an inventory with a temp db file."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    return Inventory(db_path=path), path


def test_upsert_and_search():
    inv, path = _make_inventory()
    inv.upsert({
        "path": "/tmp/test.py",
        "category": "code",
        "ext": ".py",
        "mime": "text/x-python",
        "size": 1024,
        "hash": "abc123",
        "privacy_risk": "safe",
    })
    results = inv.search(query="test.py")
    assert len(results) == 1
    assert results[0]["category"] == "code"
    inv.close()
    os.unlink(path)


def test_upsert_update():
    inv, path = _make_inventory()
    inv.upsert({
        "path": "/tmp/test.py",
        "category": "code",
        "ext": ".py",
        "mime": "text/x-python",
        "size": 1024,
        "hash": "abc",
        "privacy_risk": "safe",
    })
    inv.upsert({
        "path": "/tmp/test.py",
        "category": "code",
        "ext": ".py",
        "mime": "text/x-python",
        "size": 2048,
        "hash": "def",
        "privacy_risk": "low",
    })
    results = inv.search(query="test.py")
    assert len(results) == 1
    assert results[0]["size"] == 2048
    assert results[0]["privacy_risk"] == "low"
    inv.close()
    os.unlink(path)


def test_search_by_category():
    inv, path = _make_inventory()
    inv.upsert({"path": "/a.py", "category": "code", "ext": ".py", "mime": "", "size": 100, "hash": "", "privacy_risk": "safe"})
    inv.upsert({"path": "/b.jpg", "category": "image", "ext": ".jpg", "mime": "", "size": 200, "hash": "", "privacy_risk": "safe"})
    results = inv.search(category="code")
    assert len(results) == 1
    assert results[0]["path"] == "/a.py"
    inv.close()
    os.unlink(path)


def test_search_by_risk():
    inv, path = _make_inventory()
    inv.upsert({"path": "/safe.txt", "category": "document", "ext": ".txt", "mime": "", "size": 10, "hash": "", "privacy_risk": "safe"})
    inv.upsert({"path": "/risky.txt", "category": "document", "ext": ".txt", "mime": "", "size": 20, "hash": "", "privacy_risk": "high"})
    results = inv.search(risk="high")
    assert len(results) == 1
    assert results[0]["path"] == "/risky.txt"
    inv.close()
    os.unlink(path)


def test_stats():
    inv, path = _make_inventory()
    inv.upsert({"path": "/a.py", "category": "code", "ext": ".py", "mime": "", "size": 100, "hash": "", "privacy_risk": "safe"})
    inv.upsert({"path": "/b.py", "category": "code", "ext": ".py", "mime": "", "size": 200, "hash": "", "privacy_risk": "low"})
    inv.upsert({"path": "/c.jpg", "category": "image", "ext": ".jpg", "mime": "", "size": 300, "hash": "", "privacy_risk": "safe"})
    s = inv.stats()
    assert s["total"] == 3
    assert s["total_size"] == 600
    assert s["categories"]["code"] == 2
    assert s["categories"]["image"] == 1
    assert s["risk_summary"]["safe"] == 2
    assert s["risk_summary"]["low"] == 1
    inv.close()
    os.unlink(path)


def test_mark_registered():
    inv, path = _make_inventory()
    inv.upsert({"path": "/a.py", "category": "code", "ext": ".py", "mime": "", "size": 100, "hash": "", "privacy_risk": "safe"})
    inv.mark_registered("/a.py", "asset-001")
    results = inv.search(query="a.py")
    assert results[0]["oasyce_registered"] == "asset-001"
    inv.close()
    os.unlink(path)


def test_empty_search():
    inv, path = _make_inventory()
    results = inv.search(query="nonexistent")
    assert results == []
    inv.close()
    os.unlink(path)
