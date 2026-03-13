"""File classification by extension and MIME type."""
import mimetypes
import os
from typing import Dict

# Category mapping: extension → category
_EXT_MAP = {
    # Documents
    ".pdf": "document", ".doc": "document", ".docx": "document",
    ".txt": "document", ".md": "document", ".rtf": "document",
    ".odt": "document", ".tex": "document",
    # Spreadsheets
    ".csv": "spreadsheet", ".xls": "spreadsheet", ".xlsx": "spreadsheet",
    ".tsv": "spreadsheet", ".ods": "spreadsheet",
    # Images
    ".jpg": "image", ".jpeg": "image", ".png": "image",
    ".gif": "image", ".bmp": "image", ".svg": "image",
    ".webp": "image", ".tiff": "image", ".heic": "image",
    # Audio
    ".mp3": "audio", ".wav": "audio", ".flac": "audio",
    ".aac": "audio", ".ogg": "audio", ".m4a": "audio",
    # Video
    ".mp4": "video", ".mkv": "video", ".avi": "video",
    ".mov": "video", ".webm": "video",
    # Code
    ".py": "code", ".js": "code", ".ts": "code", ".rs": "code",
    ".go": "code", ".java": "code", ".c": "code", ".cpp": "code",
    ".h": "code", ".rb": "code", ".swift": "code",
    ".json": "data", ".yaml": "data", ".yml": "data",
    ".toml": "data", ".xml": "data", ".html": "data",
    # Archives
    ".zip": "archive", ".tar": "archive", ".gz": "archive",
    ".bz2": "archive", ".7z": "archive", ".rar": "archive",
    # Database
    ".db": "database", ".sqlite": "database", ".sqlite3": "database",
}


def classify_path(path: str) -> Dict[str, str]:
    """Classify a file by its extension and return category + mime."""
    ext = os.path.splitext(path)[1].lower()
    mime, _ = mimetypes.guess_type(path)
    category = _EXT_MAP.get(ext, "other")
    size = os.path.getsize(path)
    return {
        "category": category,
        "ext": ext,
        "mime": mime or "application/octet-stream",
        "size": size,
    }
