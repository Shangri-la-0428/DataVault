"""Tests for enhanced scanner."""
import os
import tempfile
from datavault.scanner import scan_directory, _sha256
from datavault.inventory import Inventory


def test_scan_basic():
    with tempfile.TemporaryDirectory() as d:
        for name in ["a.py", "b.txt", "c.jpg"]:
            with open(os.path.join(d, name), "w") as f:
                f.write("test")
        result = scan_directory(d, skip_privacy=True)
        assert result["total"] == 3
        assert "code" in result["categories"]
        assert "document" in result["categories"]
        assert "image" in result["categories"]


def test_scan_includes_hash():
    with tempfile.TemporaryDirectory() as d:
        fpath = os.path.join(d, "a.txt")
        with open(fpath, "w") as f:
            f.write("hello")
        result = scan_directory(d, skip_privacy=True)
        assert result["files"][0]["hash"]
        assert len(result["files"][0]["hash"]) == 64  # SHA-256 hex


def test_scan_with_privacy():
    with tempfile.TemporaryDirectory() as d:
        fpath = os.path.join(d, "data.txt")
        with open(fpath, "w") as f:
            f.write("Email: test@example.com\n")
        result = scan_directory(d, skip_privacy=False)
        assert result["files"][0]["privacy_risk"] != "safe"
        assert "risk_summary" in result


def test_scan_skip_privacy():
    with tempfile.TemporaryDirectory() as d:
        fpath = os.path.join(d, "data.txt")
        with open(fpath, "w") as f:
            f.write("Email: test@example.com\n")
        result = scan_directory(d, skip_privacy=True)
        assert result["files"][0]["privacy_risk"] == "safe"


def test_scan_with_save():
    with tempfile.TemporaryDirectory() as d:
        fpath = os.path.join(d, "a.py")
        with open(fpath, "w") as f:
            f.write("print('hi')")
        db_fd, db_path = tempfile.mkstemp(suffix=".db")
        os.close(db_fd)
        inv = Inventory(db_path=db_path)
        scan_directory(d, save=True, inventory=inv, skip_privacy=True)
        results = inv.search()
        assert len(results) == 1
        assert results[0]["category"] == "code"
        inv.close()
        os.unlink(db_path)


def test_sha256():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"hello world")
        f.flush()
        h = _sha256(f.name)
        assert len(h) == 64
        # Known SHA-256 of "hello world"
        assert h == "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
        os.unlink(f.name)


def test_scan_non_recursive():
    with tempfile.TemporaryDirectory() as d:
        with open(os.path.join(d, "top.txt"), "w") as f:
            f.write("top")
        subdir = os.path.join(d, "sub")
        os.mkdir(subdir)
        with open(os.path.join(subdir, "nested.txt"), "w") as f:
            f.write("nested")
        result = scan_directory(d, recursive=False, skip_privacy=True)
        assert result["total"] == 1


def test_scan_risk_summary():
    with tempfile.TemporaryDirectory() as d:
        with open(os.path.join(d, "clean.txt"), "w") as f:
            f.write("nothing here")
        with open(os.path.join(d, "risky.txt"), "w") as f:
            f.write("Email: user@test.com\nPhone: 13800001111\n")
        result = scan_directory(d, skip_privacy=False)
        assert "risk_summary" in result
        assert sum(result["risk_summary"].values()) == 2
