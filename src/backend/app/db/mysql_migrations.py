"""Idempotent MySQL compatibility migrations."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from sqlalchemy.engine import Connection

logger = logging.getLogger(__name__)

BANNER_BRAND_FK_NAME = "fk_banners_brand"
BANNER_BRAND_INDEX_NAME = "idx_banners_brand"
BANNER_STATUS_POSITION_INDEX_NAME = "idx_banners_status_position"
BANNER_SORT_INDEX_NAME = "idx_banners_sort"
MYSQL_COMPAT_BANNER_BRAND_VERSION = "mysql_compat_banners_brand_id_v1"


@dataclass(frozen=True)
class BannerBrandMigrationReport:
    table_exists: bool
    brand_id_added: bool
    status_position_index_added: bool
    sort_index_added: bool
    brand_index_added: bool
    brand_fk_added: bool
    brand_fk_skipped_dirty_rows: int


def _has_table(connection: Connection, table_name: str) -> bool:
    return bool(
        connection.exec_driver_sql(
            """
            SELECT 1
            FROM information_schema.TABLES
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = %s
            LIMIT 1
            """,
            (table_name,),
        ).first()
    )


def _has_column(connection: Connection, table_name: str, column_name: str) -> bool:
    return bool(
        connection.exec_driver_sql(
            """
            SELECT 1
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = %s
              AND COLUMN_NAME = %s
            LIMIT 1
            """,
            (table_name, column_name),
        ).first()
    )


def _has_index(connection: Connection, table_name: str, index_name: str) -> bool:
    return bool(
        connection.exec_driver_sql(
            """
            SELECT 1
            FROM information_schema.STATISTICS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = %s
              AND INDEX_NAME = %s
            LIMIT 1
            """,
            (table_name, index_name),
        ).first()
    )


def _has_foreign_key(connection: Connection, table_name: str, constraint_name: str) -> bool:
    return bool(
        connection.exec_driver_sql(
            """
            SELECT 1
            FROM information_schema.TABLE_CONSTRAINTS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = %s
              AND CONSTRAINT_NAME = %s
              AND CONSTRAINT_TYPE = 'FOREIGN KEY'
            LIMIT 1
            """,
            (table_name, constraint_name),
        ).first()
    )


def _dirty_banner_brand_rows(connection: Connection) -> int:
    row = connection.exec_driver_sql(
        """
        SELECT COUNT(*) AS c
        FROM banners b
        LEFT JOIN brands br ON br.id = b.brand_id
        WHERE b.brand_id IS NOT NULL
          AND br.id IS NULL
        """
    ).mappings().one()
    return int(row["c"] or 0)


def apply_mysql_compat_migrations(connection: Connection) -> list[BannerBrandMigrationReport]:
    """Apply MySQL-only migrations that CREATE TABLE IF NOT EXISTS cannot cover."""
    reports = [_ensure_banner_brand_id(connection)]
    connection.exec_driver_sql(
        """
        INSERT IGNORE INTO schema_migrations (version, applied_at)
        VALUES (%s, UTC_TIMESTAMP(3))
        """,
        (MYSQL_COMPAT_BANNER_BRAND_VERSION,),
    )
    return reports


def _ensure_banner_brand_id(connection: Connection) -> BannerBrandMigrationReport:
    if not _has_table(connection, "banners"):
        return BannerBrandMigrationReport(
            table_exists=False,
            brand_id_added=False,
            status_position_index_added=False,
            sort_index_added=False,
            brand_index_added=False,
            brand_fk_added=False,
            brand_fk_skipped_dirty_rows=0,
        )

    brand_id_added = False
    if not _has_column(connection, "banners", "brand_id"):
        connection.exec_driver_sql("ALTER TABLE banners ADD COLUMN brand_id BIGINT NULL")
        brand_id_added = True

    status_position_index_added = False
    if not _has_index(connection, "banners", BANNER_STATUS_POSITION_INDEX_NAME):
        connection.exec_driver_sql(
            f"""
            CREATE INDEX {BANNER_STATUS_POSITION_INDEX_NAME}
            ON banners (display_client, position, status)
            """
        )
        status_position_index_added = True

    sort_index_added = False
    if not _has_index(connection, "banners", BANNER_SORT_INDEX_NAME):
        connection.exec_driver_sql(
            f"CREATE INDEX {BANNER_SORT_INDEX_NAME} ON banners (sort_order, updated_at)"
        )
        sort_index_added = True

    brand_index_added = False
    if not _has_index(connection, "banners", BANNER_BRAND_INDEX_NAME):
        connection.exec_driver_sql(
            f"CREATE INDEX {BANNER_BRAND_INDEX_NAME} ON banners (brand_id)"
        )
        brand_index_added = True

    brand_fk_added = False
    dirty_rows = 0
    if not _has_foreign_key(connection, "banners", BANNER_BRAND_FK_NAME):
        dirty_rows = _dirty_banner_brand_rows(connection)
        if dirty_rows == 0:
            connection.exec_driver_sql(
                f"""
                ALTER TABLE banners
                ADD CONSTRAINT {BANNER_BRAND_FK_NAME}
                FOREIGN KEY (brand_id) REFERENCES brands(id)
                """
            )
            brand_fk_added = True
        else:
            logger.warning(
                "Skipped %s because banners has %s row(s) referencing missing brands.",
                BANNER_BRAND_FK_NAME,
                dirty_rows,
            )

    report = BannerBrandMigrationReport(
        table_exists=True,
        brand_id_added=brand_id_added,
        status_position_index_added=status_position_index_added,
        sort_index_added=sort_index_added,
        brand_index_added=brand_index_added,
        brand_fk_added=brand_fk_added,
        brand_fk_skipped_dirty_rows=dirty_rows,
    )
    logger.info("MySQL banner brand compatibility migration report: %s", report)
    return report
