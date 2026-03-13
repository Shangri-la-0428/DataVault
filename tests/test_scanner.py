import os
import tempfile
from datavault.scanner import scan_directory


def test_scan_basic():
    with tempfile.TemporaryDirectory() as d:
        for name in ["a.py", "b.txt", "c.jpg"]:
            with open(os.path.join(d, name), "w") as f:
                f.write("test")
        result = scan_directory(d)
        assert result["total"] == 3
        assert "code" in result["categories"]
        assert "document" in result["categories"]
        assert "image" in result["categories"]
