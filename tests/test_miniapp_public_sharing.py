"""Run real miniapp callbacks in a Node VM; no network or device evidence implied."""
from pathlib import Path
import subprocess


def test_public_share_runtime_contracts():
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ['node', '--test', 'tests/js/miniapp-public-sharing.cjs'],
        cwd=root, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
