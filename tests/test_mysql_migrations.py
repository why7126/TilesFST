from __future__ import annotations

from app.db.mysql_migrations import (
    BANNER_BRAND_FK_NAME,
    BANNER_BRAND_INDEX_NAME,
    BANNER_SORT_INDEX_NAME,
    BANNER_STATUS_POSITION_INDEX_NAME,
    MYSQL_COMPAT_BANNER_BRAND_VERSION,
    apply_mysql_compat_migrations,
)


class _ScalarResult:
    def __init__(self, present: bool) -> None:
        self._present = present

    def first(self) -> tuple[int] | None:
        return (1,) if self._present else None


class _MappingResult:
    def __init__(self, count: int) -> None:
        self._count = count

    def mappings(self) -> "_MappingResult":
        return self

    def one(self) -> dict[str, int]:
        return {"c": self._count}


class _FakeMySQLConnection:
    def __init__(
        self,
        *,
        table_exists: bool = True,
        has_brand_id: bool = False,
        has_status_position_index: bool = False,
        has_sort_index: bool = False,
        has_brand_index: bool = False,
        has_brand_fk: bool = False,
        dirty_brand_rows: int = 0,
    ) -> None:
        self.table_exists = table_exists
        self.has_brand_id = has_brand_id
        self.has_status_position_index = has_status_position_index
        self.has_sort_index = has_sort_index
        self.has_brand_index = has_brand_index
        self.has_brand_fk = has_brand_fk
        self.dirty_brand_rows = dirty_brand_rows
        self.statements: list[str] = []

    def exec_driver_sql(self, statement: str, params: tuple | None = None):
        normalized = " ".join(statement.split())
        if params:
            normalized = f"{normalized} params={params!r}"
        self.statements.append(normalized)

        if "information_schema.TABLES" in statement:
            return _ScalarResult(self.table_exists)
        if "information_schema.COLUMNS" in statement:
            return _ScalarResult(self.has_brand_id)
        if "information_schema.STATISTICS" in statement:
            if params and params[1] == BANNER_STATUS_POSITION_INDEX_NAME:
                return _ScalarResult(self.has_status_position_index)
            if params and params[1] == BANNER_SORT_INDEX_NAME:
                return _ScalarResult(self.has_sort_index)
            if params and params[1] == BANNER_BRAND_INDEX_NAME:
                return _ScalarResult(self.has_brand_index)
            return _ScalarResult(False)
        if "information_schema.TABLE_CONSTRAINTS" in statement:
            return _ScalarResult(self.has_brand_fk)
        if "LEFT JOIN brands" in statement:
            return _MappingResult(self.dirty_brand_rows)
        if "ADD COLUMN brand_id" in statement:
            self.has_brand_id = True
        if f"CREATE INDEX {BANNER_STATUS_POSITION_INDEX_NAME}" in statement:
            self.has_status_position_index = True
        if f"CREATE INDEX {BANNER_SORT_INDEX_NAME}" in statement:
            self.has_sort_index = True
        if f"CREATE INDEX {BANNER_BRAND_INDEX_NAME}" in statement:
            self.has_brand_index = True
        if f"ADD CONSTRAINT {BANNER_BRAND_FK_NAME}" in statement:
            self.has_brand_fk = True
        return _ScalarResult(False)


def test_apply_mysql_compat_migrations_adds_missing_banner_brand_id_idempotently() -> None:
    connection = _FakeMySQLConnection()

    report = apply_mysql_compat_migrations(connection)[0]
    second_report = apply_mysql_compat_migrations(connection)[0]

    assert report.brand_id_added is True
    assert report.status_position_index_added is True
    assert report.sort_index_added is True
    assert report.brand_index_added is True
    assert report.brand_fk_added is True
    assert second_report.brand_id_added is False
    assert second_report.status_position_index_added is False
    assert second_report.sort_index_added is False
    assert second_report.brand_index_added is False
    assert second_report.brand_fk_added is False
    assert any(
        "ALTER TABLE banners ADD COLUMN brand_id BIGINT NULL" in sql
        for sql in connection.statements
    )
    assert any(
        f"CREATE INDEX {BANNER_BRAND_INDEX_NAME}" in sql for sql in connection.statements
    )
    assert any(
        MYSQL_COMPAT_BANNER_BRAND_VERSION in str(sql) for sql in connection.statements
    )


def test_apply_mysql_compat_migrations_skips_fk_when_existing_data_is_dirty() -> None:
    connection = _FakeMySQLConnection(dirty_brand_rows=2)

    report = apply_mysql_compat_migrations(connection)[0]

    assert report.brand_id_added is True
    assert report.brand_index_added is True
    assert report.brand_fk_added is False
    assert report.brand_fk_skipped_dirty_rows == 2
    assert connection.has_brand_fk is False
