"""Local SQLite data asset inventory with incremental updates."""
import os
import sqlite3
from typing import Any, Dict, List, Optional


class Inventory:
    """Local SQLite data asset inventory."""

    DB_FILE = os.path.expanduser("~/.datavault/inventory.db")

    _CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS assets (
        path        TEXT PRIMARY KEY,
        category    TEXT,
        ext         TEXT,
        mime        TEXT,
        size        INTEGER,
        hash        TEXT,
        privacy_risk TEXT DEFAULT 'safe',
        scanned_at  TEXT DEFAULT (datetime('now')),
        oasyce_registered TEXT DEFAULT NULL
    )
    """

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or self.DB_FILE
        db_dir = os.path.dirname(self.db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
        self._conn = sqlite3.connect(self.db_path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute(self._CREATE_TABLE)
        self._conn.commit()

    def close(self):
        self._conn.close()

    def upsert(self, file_info: Dict[str, Any]):
        """Insert or update an asset record."""
        self._conn.execute(
            """INSERT INTO assets (path, category, ext, mime, size, hash, privacy_risk)
               VALUES (:path, :category, :ext, :mime, :size, :hash, :privacy_risk)
               ON CONFLICT(path) DO UPDATE SET
                 category=excluded.category, ext=excluded.ext,
                 mime=excluded.mime, size=excluded.size,
                 hash=excluded.hash, privacy_risk=excluded.privacy_risk,
                 scanned_at=datetime('now')""",
            {
                "path": file_info["path"],
                "category": file_info.get("category", "other"),
                "ext": file_info.get("ext", ""),
                "mime": file_info.get("mime", ""),
                "size": file_info.get("size", 0),
                "hash": file_info.get("hash", ""),
                "privacy_risk": file_info.get("privacy_risk", "safe"),
            },
        )
        self._conn.commit()

    def search(
        self,
        query: str = "",
        category: str = "",
        risk: str = "",
    ) -> List[Dict[str, Any]]:
        """Search asset inventory."""
        clauses = []
        params: List[Any] = []
        if query:
            clauses.append("path LIKE ?")
            params.append(f"%{query}%")
        if category:
            clauses.append("category = ?")
            params.append(category)
        if risk:
            clauses.append("privacy_risk = ?")
            params.append(risk)

        where = " AND ".join(clauses) if clauses else "1=1"
        sql = f"SELECT * FROM assets WHERE {where} ORDER BY scanned_at DESC"
        rows = self._conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]

    def stats(self) -> Dict[str, Any]:
        """Return summary statistics."""
        cur = self._conn.cursor()
        total = cur.execute("SELECT COUNT(*) FROM assets").fetchone()[0]
        total_size = cur.execute(
            "SELECT COALESCE(SUM(size), 0) FROM assets"
        ).fetchone()[0]

        cats = cur.execute(
            "SELECT category, COUNT(*) as cnt FROM assets GROUP BY category"
        ).fetchall()
        categories = {r[0]: r[1] for r in cats}

        risks = cur.execute(
            "SELECT privacy_risk, COUNT(*) as cnt FROM assets GROUP BY privacy_risk"
        ).fetchall()
        risk_summary = {r[0]: r[1] for r in risks}

        return {
            "total": total,
            "total_size": total_size,
            "categories": categories,
            "risk_summary": risk_summary,
        }

    def mark_registered(self, path: str, asset_id: str):
        """Mark an asset as registered to Oasyce."""
        self._conn.execute(
            "UPDATE assets SET oasyce_registered = ? WHERE path = ?",
            (asset_id, path),
        )
        self._conn.commit()
