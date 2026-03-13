import os
import tempfile
from datavault.classifier import classify_path


def test_classify_python():
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
        f.write(b"print('hi')")
        f.flush()
        info = classify_path(f.name)
        assert info["category"] == "code"
        os.unlink(f.name)


def test_classify_image():
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
        f.write(b"\xff\xd8\xff")
        f.flush()
        info = classify_path(f.name)
        assert info["category"] == "image"
        os.unlink(f.name)


def test_classify_unknown():
    with tempfile.NamedTemporaryFile(suffix=".xyz123", delete=False) as f:
        f.write(b"data")
        f.flush()
        info = classify_path(f.name)
        assert info["category"] == "other"
        os.unlink(f.name)
