"""Disposable remote deployment smoke; no real backend, identity, or TLS proof."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile
import uuid


ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", default="tilesfst-workbuddy:local-req0132")
    parser.add_argument("--base-image", default="tilesfst-tilesfst-backend")
    args = parser.parse_args()
    project = "wb-remote-" + uuid.uuid4().hex[:10]
    with tempfile.TemporaryDirectory(prefix="wb-remote-") as directory:
        # Empty synthetic mapping verifies refusal; no backend credential is needed.
        secret = Path(directory) / "workbuddy-credentials.json"
        secret.write_text("{}", encoding="utf-8")
        secret.chmod(0o444)
        Path(directory).chmod(0o755)
        env = {key: value for key, value in os.environ.items()
               if not key.startswith(("COMPOSE_", "WORKBUDDY_", "TILESFST_", "HOST_PORT_"))}
        env.update(WORKBUDDY_MCP_IMAGE=args.image, WORKBUDDY_BASE_IMAGE=args.base_image,
                   WORKBUDDY_SECRET_DIR=directory, TILESFST_API_BASE_URL="http://127.0.0.1:9",
                   HOST_PORT_WORKBUDDY_MCP="0")
        command = ["docker", "compose", "--env-file", "/dev/null", "-p", project,
                   "-f", str(ROOT / "deploy/prod/compose.workbuddy.yml")]

        def compose(*arguments):
            result = subprocess.run([*command, *arguments], env=env, capture_output=True,
                                    text=True, timeout=120)
            if result.returncode:
                raise RuntimeError("Isolated compose command failed: " + arguments[0])
            return result.stdout

        def execute(code):
            return compose("exec", "-T", "workbuddy-mcp", "/app/.venv/bin/python", "-c", code)

        model = json.loads(compose("config", "--format", "json"))
        service = model["services"]["workbuddy-mcp"]
        assert service["read_only"] and service["cap_drop"] == ["ALL"]
        assert service["ports"][0]["host_ip"] == "127.0.0.1"
        assert "TILESFST_CONNECTOR_TOKEN" not in service["environment"]
        try:
            compose("up", "-d", "--no-build", "--pull", "never", "--wait", "--wait-timeout", "45")
            execute("""
import json, os, urllib.request, urllib.error
assert os.getuid() == 10001
assert json.load(urllib.request.urlopen('http://127.0.0.1:8010/health'))['ok']
for headers in ({}, {'Authorization': 'Bearer synthetic-invalid'}):
    request = urllib.request.Request('http://127.0.0.1:8010/mcp', data=b'{}', headers=headers)
    try:
        urllib.request.urlopen(request)
        raise AssertionError('Anonymous or invalid credential accepted')
    except urllib.error.HTTPError as error:
        assert error.code == 401
from src.mcp.workbuddy.adapters.idempotency import WriteJournal
result = WriteJournal('/app/data/workbuddy/idempotency').execute(
    'synthetic', 'smoke-key', 'test', {}, lambda: {'ok': True})
assert result['ok']
""")
            compose("restart", "workbuddy-mcp")
            execute("""
from src.mcp.workbuddy.adapters.idempotency import WriteJournal
def must_not_execute():
    raise AssertionError('Duplicate executed')
result = WriteJournal('/app/data/workbuddy/idempotency').execute(
    'synthetic', 'smoke-key', 'test', {}, must_not_execute)
assert result['error'] == 'duplicate_operation'
""")
            print(json.dumps({"result": "passed", "checks": ["compose-security", "non-root",
                "health", "anonymous-denied", "invalid-credential-denied", "journal-write",
                "journal-restart"], "boundary": "local container; no real backend or TLS"}))
        finally:
            compose("down", "--volumes", "--remove-orphans")


if __name__ == "__main__":
    main()
