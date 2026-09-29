"""Guard isolation and cleanup without starting Docker in ordinary pytest runs."""

import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def driver(monkeypatch):
    monkeypatch.setattr(sys, "dont_write_bytecode", True)
    spec = importlib.util.spec_from_file_location(
        "workbuddy_acceptance_driver", ROOT / "deploy/scripts/verify-workbuddy-local.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_compose_cannot_attach_business_data_or_publish_ports():
    config = yaml.safe_load((ROOT / "deploy/local/compose.workbuddy-acceptance.yml").read_text())
    assert config["networks"]["acceptance"]["internal"] is True
    assert set(config["volumes"]) == {"database", "objects", "scratch", "journal"}
    assert all(value is None for value in config["volumes"].values())
    assert config["services"]["acceptance"]["environment"]["PYTHONPYCACHEPREFIX"].startswith("/tmp/")
    for service in config["services"].values():
        assert not any(key in service for key in ("ports", "container_name", "env_file", "network_mode"))
        for mount in service.get("volumes", []):
            if mount.startswith("../"):
                assert mount.endswith(":ro")
                assert "data/" not in mount and ".env" not in mount


def test_mcp_child_does_not_receive_storage_or_login_credentials(driver, monkeypatch):
    monkeypatch.setenv("TILESFST_CONNECTOR_TOKEN", "synthetic-api-token")
    monkeypatch.setenv("ADMIN_INITIAL_PASSWORD", "synthetic-login-secret")
    monkeypatch.setenv("OBJECT_STORAGE_SECRET_KEY", "synthetic-storage-secret")
    def run(command, **kwargs):
        assert "ADMIN_INITIAL_PASSWORD" not in kwargs["env"]
        assert "OBJECT_STORAGE_SECRET_KEY" not in kwargs["env"]
        assert kwargs["env"]["TILESFST_CONNECTOR_TOKEN"] == "synthetic-api-token"
        responses = [
            {"id": 3, "result": {"tools": [{"name": "search_tile_skus"}]}},
            {"id": 2, "result": {"isError": False, "content": [{"type": "text", "text": '{"ok": true}'}]}},
        ]
        return SimpleNamespace(returncode=0, stdout="\n".join(map(json.dumps, responses)), stderr="")
    monkeypatch.setattr(driver.subprocess, "run", run)
    assert driver.mcp("search_tile_skus", {})["ok"] is True


@pytest.mark.parametrize("failure", [False, True])
def test_driver_isolates_env_and_always_cleans_own_containers(driver, monkeypatch, capsys, failure):
    calls = []
    monkeypatch.setenv("COMPOSE_PROJECT_NAME", "business-project")
    monkeypatch.setenv("TILESFST_CONNECTOR_TOKEN", "synthetic-business-token")
    monkeypatch.setenv("OBJECT_STORAGE_SECRET_KEY", "synthetic-business-secret")

    def run(command, **kwargs):
        calls.append((command, kwargs["env"]))
        return SimpleNamespace(returncode=int(failure and "run" in command),
                               stdout="sensitive-output-must-not-escape", stderr="secret")

    monkeypatch.setattr(driver.subprocess, "run", run)
    if failure:
        with pytest.raises(RuntimeError):
            driver.orchestrate()
    else:
        driver.orchestrate()
    assert calls[-1][0][-1] == "down"
    for command, env in calls:
        assert command[command.index("-p") + 1].startswith("wb-req0132-")
        assert command[command.index("--env-file") + 1] == driver.os.devnull
        assert "--volumes" not in command and "-v" not in command
        assert "COMPOSE_PROJECT_NAME" not in env
        assert "TILESFST_CONNECTOR_TOKEN" not in env
        assert env["OBJECT_STORAGE_SECRET_KEY"] != "synthetic-business-secret"
    assert "sensitive-output" not in capsys.readouterr().out
