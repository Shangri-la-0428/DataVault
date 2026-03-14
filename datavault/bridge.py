"""Oasyce bridge — connect DataVault with Oasyce protocol."""
from typing import Any, Dict, List, Optional


class OasyceBridge:
    """Connect DataVault with Oasyce protocol."""

    def check_oasyce_available(self) -> bool:
        """Check if oasyce package is installed."""
        try:
            import oasyce_plugin  # noqa: F401
            return True
        except ImportError:
            return False

    def register_asset(
        self,
        path: str,
        owner: str,
        tags: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Register a single asset to Oasyce."""
        try:
            from oasyce_plugin import register
        except ImportError:
            return {
                "success": False,
                "error": "oasyce_plugin not installed. Run: pip install datavault[oasyce]",
            }

        try:
            result = register(path=path, owner=owner, tags=tags or [])
            return {"success": True, "asset_id": result.get("asset_id", ""), **result}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def bulk_register(
        self,
        paths: List[str],
        owner: str,
        tags: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Register multiple assets to Oasyce."""
        return [self.register_asset(p, owner, tags) for p in paths]
