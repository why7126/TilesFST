from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check-mysql-schema-drift.py"
SPEC = importlib.util.spec_from_file_location("check_mysql_schema_drift_script", SCRIPT)
assert SPEC and SPEC.loader
check_mysql_schema_drift_script = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_mysql_schema_drift_script)


def test_parse_expected_schema_ignores_constraints_and_indexes() -> None:
    schema = """
    CREATE TABLE IF NOT EXISTS brands (
      id BIGINT AUTO_INCREMENT PRIMARY KEY,
      name VARCHAR(128) NOT NULL UNIQUE,
      status VARCHAR(32) NOT NULL DEFAULT 'ENABLED',
      CONSTRAINT chk_brands_status CHECK (status IN ('ENABLED', 'DISABLED')),
      UNIQUE KEY uq_brands_name (name),
      INDEX idx_brands_status (status)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """

    expected = check_mysql_schema_drift_script.parse_expected_schema(schema)

    assert expected == {"brands": {"id", "name", "status"}}


def test_compare_schema_reports_missing_tables_and_columns() -> None:
    expected = {
        "brands": {"id", "name", "logo_object_key"},
        "banners": {"id", "brand_id"},
    }
    actual = {
        "brands": {"id", "name", "legacy_note"},
        "users": {"id"},
    }

    report = check_mysql_schema_drift_script.compare_schema(expected, actual)

    assert report["missing_tables"] == ["banners"]
    assert report["extra_tables"] == ["users"]
    assert report["missing_columns"] == {"brands": ["logo_object_key"]}
    assert report["extra_columns"] == {"brands": ["legacy_note"]}
    assert check_mysql_schema_drift_script.has_blocking_drift(report) is True
