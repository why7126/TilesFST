from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "deploy" / "scripts" / "media-maintenance.sh"


def test_media_maintenance_script_has_valid_shell_syntax() -> None:
    result = subprocess.run(["bash", "-n", str(SCRIPT)], capture_output=True, text=True)

    assert result.returncode == 0, result.stderr


def test_media_maintenance_script_defaults_to_read_only_audit() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    assert 'DOMAIN="${1:-prod}"' in content
    assert 'ENVIRONMENT="${2:-mysql-tencent-cos}"' in content
    assert 'TASK="${3:-object-key-audit}"' in content
    assert "--apply --confirm-backup" in content
    assert "不输出 env 内容、数据库连接串或对象存储密钥" in content
