from __future__ import annotations

from app.db.mysql_migrations import (
    BANNER_GALLERY_ASSET_FK_NAME,
    BANNER_GALLERY_ASSET_INDEX_NAME,
    BANNER_BRAND_FK_NAME,
    BANNER_BRAND_INDEX_NAME,
    BANNER_SORT_INDEX_NAME,
    BANNER_STATUS_POSITION_INDEX_NAME,
    BANNER_TOPIC_FK_NAME,
    BANNER_TOPIC_INDEX_NAME,
    BANNER_CHECK_CONSTRAINTS,
    BANNER_WRITE_FIELD_COLUMNS,
    MYSQL_COMPAT_BANNER_BRAND_VERSION,
    MYSQL_COMPAT_BANNER_CHECKS_VERSION,
    MYSQL_COMPAT_BANNER_WRITE_FIELDS_VERSION,
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
        existing_columns: set[str] | None = None,
        has_status_position_index: bool = False,
        has_sort_index: bool = False,
        has_brand_index: bool = False,
        has_topic_index: bool = False,
        has_gallery_asset_index: bool = False,
        has_brand_fk: bool = False,
        has_topic_fk: bool = False,
        has_gallery_asset_fk: bool = False,
        dirty_fk_rows: dict[str, int] | None = None,
        check_constraints: dict[str, str] | None = None,
    ) -> None:
        self.table_exists = table_exists
        self.columns = set(existing_columns or ())
        self.has_status_position_index = has_status_position_index
        self.has_sort_index = has_sort_index
        self.has_brand_index = has_brand_index
        self.has_topic_index = has_topic_index
        self.has_gallery_asset_index = has_gallery_asset_index
        self.foreign_keys = {
            BANNER_BRAND_FK_NAME: has_brand_fk,
            BANNER_TOPIC_FK_NAME: has_topic_fk,
            BANNER_GALLERY_ASSET_FK_NAME: has_gallery_asset_fk,
        }
        self.dirty_fk_rows = dirty_fk_rows or {}
        self.check_constraints = dict(check_constraints or {})
        self.statements: list[str] = []

    def exec_driver_sql(self, statement: str, params: tuple | None = None):
        normalized = " ".join(statement.split())
        if params:
            normalized = f"{normalized} params={params!r}"
        self.statements.append(normalized)

        if "information_schema.TABLES" in statement:
            return _ScalarResult(self.table_exists)
        if "information_schema.COLUMNS" in statement:
            return _ScalarResult(bool(params and params[1] in self.columns))
        if "information_schema.STATISTICS" in statement:
            if params and params[1] == BANNER_STATUS_POSITION_INDEX_NAME:
                return _ScalarResult(self.has_status_position_index)
            if params and params[1] == BANNER_SORT_INDEX_NAME:
                return _ScalarResult(self.has_sort_index)
            if params and params[1] == BANNER_BRAND_INDEX_NAME:
                return _ScalarResult(self.has_brand_index)
            if params and params[1] == BANNER_TOPIC_INDEX_NAME:
                return _ScalarResult(self.has_topic_index)
            if params and params[1] == BANNER_GALLERY_ASSET_INDEX_NAME:
                return _ScalarResult(self.has_gallery_asset_index)
            return _ScalarResult(False)
        if "information_schema.TABLE_CONSTRAINTS" in statement:
            if "CONSTRAINT_TYPE = 'CHECK'" in statement:
                if params and params[1] in self.check_constraints:
                    return _CheckConstraintResult(self.check_constraints[params[1]])
                return _CheckConstraintResult(None)
            return _ScalarResult(bool(params and self.foreign_keys.get(params[1], False)))
        if "LEFT JOIN brands" in statement:
            return _MappingResult(self.dirty_fk_rows.get("brand_id", 0))
        if "LEFT JOIN topics" in statement:
            return _MappingResult(self.dirty_fk_rows.get("topic_id", 0))
        if "LEFT JOIN tile_images" in statement:
            return _MappingResult(self.dirty_fk_rows.get("sku_gallery_asset_id", 0))
        if "ADD COLUMN" in statement:
            for column_name in BANNER_WRITE_FIELD_COLUMNS:
                if f"ADD COLUMN {column_name} " in statement:
                    self.columns.add(column_name)
        if f"CREATE INDEX {BANNER_STATUS_POSITION_INDEX_NAME}" in statement:
            self.has_status_position_index = True
        if f"CREATE INDEX {BANNER_SORT_INDEX_NAME}" in statement:
            self.has_sort_index = True
        if f"CREATE INDEX {BANNER_BRAND_INDEX_NAME}" in statement:
            self.has_brand_index = True
        if f"CREATE INDEX {BANNER_TOPIC_INDEX_NAME}" in statement:
            self.has_topic_index = True
        if f"CREATE INDEX {BANNER_GALLERY_ASSET_INDEX_NAME}" in statement:
            self.has_gallery_asset_index = True
        if f"ADD CONSTRAINT {BANNER_BRAND_FK_NAME}" in statement:
            self.foreign_keys[BANNER_BRAND_FK_NAME] = True
        if f"ADD CONSTRAINT {BANNER_TOPIC_FK_NAME}" in statement:
            self.foreign_keys[BANNER_TOPIC_FK_NAME] = True
        if f"ADD CONSTRAINT {BANNER_GALLERY_ASSET_FK_NAME}" in statement:
            self.foreign_keys[BANNER_GALLERY_ASSET_FK_NAME] = True
        for constraint_name, (check_clause, _) in BANNER_CHECK_CONSTRAINTS.items():
            if f"DROP CHECK {constraint_name}" in statement:
                self.check_constraints.pop(constraint_name, None)
            if f"ADD CONSTRAINT {constraint_name}" in statement:
                self.check_constraints[constraint_name] = check_clause
        return _ScalarResult(False)


class _CheckConstraintResult:
    def __init__(self, clause: str | None) -> None:
        self._clause = clause

    def first(self) -> tuple[str] | None:
        return (self._clause,) if self._clause is not None else None


def test_apply_mysql_compat_migrations_adds_missing_banner_brand_id_idempotently() -> None:
    connection = _FakeMySQLConnection()

    report = apply_mysql_compat_migrations(connection)[0]
    second_report = apply_mysql_compat_migrations(connection)[0]

    assert report.columns_added == tuple(BANNER_WRITE_FIELD_COLUMNS)
    assert report.brand_id_added is True
    assert report.status_position_index_added is True
    assert report.sort_index_added is True
    assert report.brand_index_added is True
    assert report.topic_index_added is True
    assert report.gallery_asset_index_added is True
    assert report.brand_fk_added is True
    assert report.topic_fk_added is True
    assert report.gallery_asset_fk_added is True
    assert report.check_constraints_rebuilt == tuple(BANNER_CHECK_CONSTRAINTS)
    assert second_report.columns_added == ()
    assert second_report.brand_id_added is False
    assert second_report.status_position_index_added is False
    assert second_report.sort_index_added is False
    assert second_report.brand_index_added is False
    assert second_report.topic_index_added is False
    assert second_report.gallery_asset_index_added is False
    assert second_report.brand_fk_added is False
    assert second_report.topic_fk_added is False
    assert second_report.gallery_asset_fk_added is False
    assert second_report.check_constraints_rebuilt == ()
    for column_name, column_definition in BANNER_WRITE_FIELD_COLUMNS.items():
        assert any(
            f"ALTER TABLE banners ADD COLUMN {column_name} {column_definition}" in sql
            for sql in connection.statements
        )
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
    assert any(
        MYSQL_COMPAT_BANNER_WRITE_FIELDS_VERSION in str(sql)
        for sql in connection.statements
    )
    assert any(
        MYSQL_COMPAT_BANNER_CHECKS_VERSION in str(sql)
        for sql in connection.statements
    )


def test_apply_mysql_compat_migrations_skips_fk_when_existing_data_is_dirty() -> None:
    connection = _FakeMySQLConnection(
        dirty_fk_rows={"brand_id": 2, "topic_id": 3, "sku_gallery_asset_id": 4}
    )

    report = apply_mysql_compat_migrations(connection)[0]

    assert report.brand_id_added is True
    assert report.brand_index_added is True
    assert report.brand_fk_added is False
    assert report.topic_fk_added is False
    assert report.gallery_asset_fk_added is False
    assert report.brand_fk_skipped_dirty_rows == 2
    assert report.topic_fk_skipped_dirty_rows == 3
    assert report.gallery_asset_fk_skipped_dirty_rows == 4
    assert connection.foreign_keys[BANNER_BRAND_FK_NAME] is False
    assert connection.foreign_keys[BANNER_TOPIC_FK_NAME] is False
    assert connection.foreign_keys[BANNER_GALLERY_ASSET_FK_NAME] is False


def test_apply_mysql_compat_migrations_rebuilds_legacy_banner_check_constraints() -> None:
    connection = _FakeMySQLConnection(
        existing_columns=set(BANNER_WRITE_FIELD_COLUMNS),
        has_status_position_index=True,
        has_sort_index=True,
        has_brand_index=True,
        has_topic_index=True,
        has_gallery_asset_index=True,
        has_brand_fk=True,
        has_topic_fk=True,
        has_gallery_asset_fk=True,
        check_constraints={
            "chk_banners_display_client": "display_client = 'MINIAPP_HOME'",
            "chk_banners_position": "position in ('MINIAPP_HOME_CAROUSEL')",
            "chk_banners_jump_type": "jump_type in ('SKU_DETAIL', 'NO_JUMP')",
            "chk_banners_image_source": (
                "image_source in ('sku_main_image', 'sku_gallery_image', 'custom_upload')"
            ),
        },
    )

    report = apply_mysql_compat_migrations(connection)[0]

    assert report.columns_added == ()
    assert report.check_constraints_rebuilt == (
        "chk_banners_position",
        "chk_banners_jump_type",
        "chk_banners_image_source",
    )
    assert "brand_logo" in connection.check_constraints["chk_banners_image_source"]
    assert "BRAND_DETAIL" in connection.check_constraints["chk_banners_jump_type"]
    assert (
        "MINIAPP_BRAND_LIST_CAROUSEL"
        in connection.check_constraints["chk_banners_position"]
    )
    assert any("DROP CHECK chk_banners_image_source" in sql for sql in connection.statements)
