"""Tests for Oasyce bridge."""
import sys
import types
from unittest import mock
from datavault.bridge import OasyceBridge


def test_check_oasyce_not_available():
    with mock.patch.dict(sys.modules, {"oasyce_plugin": None}):
        bridge = OasyceBridge()
        assert bridge.check_oasyce_available() is False


def test_register_without_oasyce():
    with mock.patch.dict(sys.modules, {"oasyce_plugin": None}):
        bridge = OasyceBridge()
        result = bridge.register_asset("/tmp/test.txt", owner="owner-key")
        assert result["success"] is False
        assert "not installed" in result["error"]


def test_register_with_mock_oasyce():
    # Create a mock oasyce_plugin module
    mock_module = types.ModuleType("oasyce_plugin")
    mock_module.register = mock.Mock(return_value={"asset_id": "asset-123"})

    with mock.patch.dict(sys.modules, {"oasyce_plugin": mock_module}):
        bridge = OasyceBridge()
        assert bridge.check_oasyce_available() is True

        result = bridge.register_asset("/tmp/test.txt", owner="owner-key", tags=["data"])
        assert result["success"] is True
        assert result["asset_id"] == "asset-123"
        mock_module.register.assert_called_once_with(
            path="/tmp/test.txt", owner="owner-key", tags=["data"]
        )


def test_bulk_register_without_oasyce():
    with mock.patch.dict(sys.modules, {"oasyce_plugin": None}):
        bridge = OasyceBridge()
        results = bridge.bulk_register(["/a.txt", "/b.txt"], owner="owner-key")
        assert len(results) == 2
        assert all(not r["success"] for r in results)


def test_bulk_register_with_mock_oasyce():
    mock_module = types.ModuleType("oasyce_plugin")
    call_count = 0

    def mock_register(path, owner, tags):
        nonlocal call_count
        call_count += 1
        return {"asset_id": f"asset-{call_count}"}

    mock_module.register = mock_register

    with mock.patch.dict(sys.modules, {"oasyce_plugin": mock_module}):
        bridge = OasyceBridge()
        results = bridge.bulk_register(["/a.txt", "/b.txt"], owner="owner-key")
        assert len(results) == 2
        assert results[0]["asset_id"] == "asset-1"
        assert results[1]["asset_id"] == "asset-2"


def test_register_exception_handling():
    mock_module = types.ModuleType("oasyce_plugin")
    mock_module.register = mock.Mock(side_effect=RuntimeError("network error"))

    with mock.patch.dict(sys.modules, {"oasyce_plugin": mock_module}):
        bridge = OasyceBridge()
        result = bridge.register_asset("/tmp/test.txt", owner="owner-key")
        assert result["success"] is False
        assert "network error" in result["error"]
