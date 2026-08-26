"""Idempotent MySQL compatibility migrations."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from sqlalchemy.engine import Connection

logger = logging.getLogger(__name__)

BANNER_BRAND_FK_NAME = "fk_banners_brand"
BANNER_TOPIC_FK_NAME = "fk_banners_topic"
BANNER_GALLERY_ASSET_FK_NAME = "fk_banners_gallery_asset"
BANNER_BRAND_INDEX_NAME = "idx_banners_brand"
BANNER_TOPIC_INDEX_NAME = "idx_banners_topic"
BANNER_GALLERY_ASSET_INDEX_NAME = "idx_banners_gallery_asset"
BANNER_STATUS_POSITION_INDEX_NAME = "idx_banners_status_position"
BANNER_SORT_INDEX_NAME = "idx_banners_sort"
MYSQL_COMPAT_BANNER_BRAND_VERSION = "mysql_compat_banners_brand_id_v1"
MYSQL_COMPAT_BANNER_WRITE_FIELDS_VERSION = "mysql_compat_banners_write_fields_v2"
MYSQL_COMPAT_BANNER_CHECKS_VERSION = "mysql_compat_banners_checks_v3"
MYSQL_COMPAT_TASK_TRACE_VERSION = "mysql_compat_task_trace_v1"
MYSQL_COMPAT_CLIENT_REQUEST_ID_VERSION = "mysql_compat_client_request_id_v1"
MYSQL_COMPAT_BEHAVIOR_TRACE_VERSION = "mysql_compat_behavior_trace_v1"
MYSQL_COMPAT_BRAND_CERTIFICATE_IMAGES_VERSION = "mysql_compat_brand_certificate_images_v1"
MYSQL_COMPAT_TILES_PUBLISHED_AT_VERSION = "mysql_compat_tiles_published_at_v1"
MYSQL_COMPAT_USERS_THEME_MODE_VERSION = "mysql_compat_users_theme_mode_v1"
MYSQL_COMPAT_PERFORMANCE_EVENTS_VERSION = "mysql_compat_performance_events_v1"

BANNER_WRITE_FIELD_COLUMNS: dict[str, str] = {
    "image_source": "VARCHAR(64) NOT NULL DEFAULT 'custom_upload'",
    "sku_gallery_asset_id": "BIGINT NULL",
    "topic_id": "BIGINT NULL",
    "brand_id": "BIGINT NULL",
    "valid_from": "VARCHAR(64) NULL",
    "valid_to": "VARCHAR(64) NULL",
    "remark": "TEXT NULL",
}

BANNER_CHECK_CONSTRAINTS: dict[str, tuple[str, tuple[str, ...]]] = {
    "chk_banners_display_client": (
        "display_client = 'MINIAPP_HOME'",
        ("MINIAPP_HOME",),
    ),
    "chk_banners_position": (
        "position IN ('MINIAPP_HOME_CAROUSEL', 'MINIAPP_BRAND_LIST_CAROUSEL')",
        ("MINIAPP_HOME_CAROUSEL", "MINIAPP_BRAND_LIST_CAROUSEL"),
    ),
    "chk_banners_jump_type": (
        "jump_type IN ('SKU_DETAIL', 'BRAND_DETAIL', 'EXTERNAL_LINK', 'TOPIC_PAGE', 'NO_JUMP')",
        ("SKU_DETAIL", "BRAND_DETAIL", "EXTERNAL_LINK", "TOPIC_PAGE", "NO_JUMP"),
    ),
    "chk_banners_image_source": (
        "image_source IN ('sku_main_image', 'sku_gallery_image', 'custom_upload', 'topic_cover', 'brand_logo')",
        ("sku_main_image", "sku_gallery_image", "custom_upload", "topic_cover", "brand_logo"),
    ),
}


@dataclass(frozen=True)
class BannerBrandMigrationReport:
    table_exists: bool
    columns_added: tuple[str, ...]
    brand_id_added: bool
    status_position_index_added: bool
    sort_index_added: bool
    brand_index_added: bool
    topic_index_added: bool
    gallery_asset_index_added: bool
    brand_fk_added: bool
    topic_fk_added: bool
    gallery_asset_fk_added: bool
    check_constraints_rebuilt: tuple[str, ...]
    brand_fk_skipped_dirty_rows: int
    topic_fk_skipped_dirty_rows: int
    gallery_asset_fk_skipped_dirty_rows: int


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


def _check_constraint_clause(
    connection: Connection, table_name: str, constraint_name: str
) -> str | None:
    row = connection.exec_driver_sql(
        """
        SELECT cc.CHECK_CLAUSE
        FROM information_schema.TABLE_CONSTRAINTS tc
        JOIN information_schema.CHECK_CONSTRAINTS cc
          ON cc.CONSTRAINT_SCHEMA = tc.CONSTRAINT_SCHEMA
         AND cc.CONSTRAINT_NAME = tc.CONSTRAINT_NAME
        WHERE tc.TABLE_SCHEMA = DATABASE()
          AND tc.TABLE_NAME = %s
          AND tc.CONSTRAINT_NAME = %s
          AND tc.CONSTRAINT_TYPE = 'CHECK'
        LIMIT 1
        """,
        (table_name, constraint_name),
    ).first()
    return str(row[0]) if row else None


def _dirty_banner_fk_rows(connection: Connection, column_name: str, target_table: str) -> int:
    row = connection.exec_driver_sql(
        f"""
        SELECT COUNT(*) AS c
        FROM banners b
        LEFT JOIN {target_table} target ON target.id = b.{column_name}
        WHERE b.{column_name} IS NOT NULL
          AND target.id IS NULL
        """
    ).mappings().one()
    return int(row["c"] or 0)


def apply_mysql_compat_migrations(connection: Connection) -> list[BannerBrandMigrationReport]:
    """Apply MySQL-only migrations that CREATE TABLE IF NOT EXISTS cannot cover."""
    reports = [_ensure_banner_brand_id(connection)]
    _ensure_task_trace_support(connection)
    _ensure_brand_certificate_images_support(connection)
    _ensure_tiles_published_at_support(connection)
    _ensure_users_theme_mode_support(connection)
    _ensure_performance_events_support(connection)
    connection.exec_driver_sql(
        """
        INSERT IGNORE INTO schema_migrations (version, applied_at)
        VALUES (%s, UTC_TIMESTAMP(3))
        """,
        (MYSQL_COMPAT_BANNER_BRAND_VERSION,),
    )
    connection.exec_driver_sql(
        """
        INSERT IGNORE INTO schema_migrations (version, applied_at)
        VALUES (%s, UTC_TIMESTAMP(3))
        """,
        (MYSQL_COMPAT_BANNER_WRITE_FIELDS_VERSION,),
    )
    connection.exec_driver_sql(
        """
        INSERT IGNORE INTO schema_migrations (version, applied_at)
        VALUES (%s, UTC_TIMESTAMP(3))
        """,
        (MYSQL_COMPAT_BANNER_CHECKS_VERSION,),
    )
    connection.exec_driver_sql(
        """
        INSERT IGNORE INTO schema_migrations (version, applied_at)
        VALUES (%s, UTC_TIMESTAMP(3))
        """,
        (MYSQL_COMPAT_TASK_TRACE_VERSION,),
    )
    _ensure_client_request_id_support(connection)
    _ensure_behavior_trace_support(connection)
    connection.exec_driver_sql(
        """
        INSERT IGNORE INTO schema_migrations (version, applied_at)
        VALUES (%s, UTC_TIMESTAMP(3))
        """,
        (MYSQL_COMPAT_CLIENT_REQUEST_ID_VERSION,),
    )
    connection.exec_driver_sql(
        """
        INSERT IGNORE INTO schema_migrations (version, applied_at)
        VALUES (%s, UTC_TIMESTAMP(3))
        """,
        (MYSQL_COMPAT_BEHAVIOR_TRACE_VERSION,),
    )
    connection.exec_driver_sql(
        """
        INSERT IGNORE INTO schema_migrations (version, applied_at)
        VALUES (%s, UTC_TIMESTAMP(3))
        """,
        (MYSQL_COMPAT_BRAND_CERTIFICATE_IMAGES_VERSION,),
    )
    connection.exec_driver_sql(
        """
        INSERT IGNORE INTO schema_migrations (version, applied_at)
        VALUES (%s, UTC_TIMESTAMP(3))
        """,
        (MYSQL_COMPAT_TILES_PUBLISHED_AT_VERSION,),
    )
    connection.exec_driver_sql(
        """
        INSERT IGNORE INTO schema_migrations (version, applied_at)
        VALUES (%s, UTC_TIMESTAMP(3))
        """,
        (MYSQL_COMPAT_USERS_THEME_MODE_VERSION,),
    )
    connection.exec_driver_sql(
        """
        INSERT IGNORE INTO schema_migrations (version, applied_at)
        VALUES (%s, UTC_TIMESTAMP(3))
        """,
        (MYSQL_COMPAT_PERFORMANCE_EVENTS_VERSION,),
    )
    return reports


def _ensure_performance_events_support(connection: Connection) -> None:
    if not _has_table(connection, "performance_events"):
        connection.exec_driver_sql(
            """
            CREATE TABLE performance_events (
              id CHAR(36) PRIMARY KEY,
              client_type VARCHAR(32) NOT NULL,
              page_key VARCHAR(120) NOT NULL,
              app_version VARCHAR(64),
              network_type VARCHAR(32),
              device_class VARCHAR(32),
              metric_name VARCHAR(64) NOT NULL,
              duration_ms INT NOT NULL,
              sample_rate DECIMAL(5,4) NOT NULL DEFAULT 1.0000,
              occurred_at VARCHAR(64) NOT NULL,
              server_received_at VARCHAR(64) NOT NULL,
              request_id VARCHAR(128),
              metadata TEXT,
              CONSTRAINT chk_performance_events_client_type CHECK (client_type IN ('web_admin', 'web_catalog', 'wechat_miniapp')),
              CONSTRAINT chk_performance_events_duration CHECK (duration_ms >= 0),
              CONSTRAINT chk_performance_events_sample_rate CHECK (sample_rate >= 0 AND sample_rate <= 1),
              INDEX idx_performance_events_received (server_received_at),
              INDEX idx_performance_events_client_page_metric (client_type, page_key, metric_name, server_received_at),
              INDEX idx_performance_events_version (app_version, server_received_at),
              INDEX idx_performance_events_network (network_type, device_class, server_received_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
        )


def _ensure_users_theme_mode_support(connection: Connection) -> None:
    if not _has_table(connection, "users"):
        return
    if not _has_column(connection, "users", "theme_mode"):
        connection.exec_driver_sql(
            "ALTER TABLE users ADD COLUMN theme_mode VARCHAR(32) NOT NULL DEFAULT 'system'"
        )


def _ensure_tiles_published_at_support(connection: Connection) -> None:
    if not _has_table(connection, "tiles"):
        return
    if not _has_column(connection, "tiles", "published_at"):
        connection.exec_driver_sql("ALTER TABLE tiles ADD COLUMN published_at VARCHAR(64) NULL")
        connection.exec_driver_sql(
            """
            UPDATE tiles
            SET published_at = updated_at
            WHERE status = 'PUBLISHED' AND published_at IS NULL
            """
        )
    if not _has_index(connection, "tiles", "idx_tiles_published_at"):
        connection.exec_driver_sql("CREATE INDEX idx_tiles_published_at ON tiles (published_at)")
    if not _has_column(connection, "tiles", "recall_pin_sort_order"):
        connection.exec_driver_sql(
            "ALTER TABLE tiles ADD COLUMN recall_pin_sort_order INT NOT NULL DEFAULT 9999"
        )
    if not _has_column(connection, "tiles", "recall_pin_starts_at"):
        connection.exec_driver_sql("ALTER TABLE tiles ADD COLUMN recall_pin_starts_at VARCHAR(64) NULL")
    if not _has_column(connection, "tiles", "recall_pin_ends_at"):
        connection.exec_driver_sql("ALTER TABLE tiles ADD COLUMN recall_pin_ends_at VARCHAR(64) NULL")
    if not _has_index(connection, "tiles", "idx_tiles_recall_pin"):
        connection.exec_driver_sql(
            "CREATE INDEX idx_tiles_recall_pin ON tiles "
            "(recall_pin_sort_order, recall_pin_starts_at, recall_pin_ends_at)"
        )


def _ensure_brand_certificate_images_support(connection: Connection) -> None:
    if _has_table(connection, "brand_certificate_images"):
        return
    connection.exec_driver_sql(
        """
        CREATE TABLE brand_certificate_images (
          id BIGINT AUTO_INCREMENT PRIMARY KEY,
          certificate_id BIGINT NOT NULL,
          file_url VARCHAR(768) NOT NULL,
          file_key VARCHAR(512) NOT NULL,
          file_name VARCHAR(255) NOT NULL,
          file_mime_type VARCHAR(128) NOT NULL,
          file_size_bytes BIGINT NOT NULL,
          is_main TINYINT NOT NULL DEFAULT 0,
          sort_order INT NOT NULL DEFAULT 0,
          created_at VARCHAR(64) NOT NULL,
          updated_at VARCHAR(64) NOT NULL,
          CONSTRAINT fk_brand_certificate_images_certificate
            FOREIGN KEY(certificate_id) REFERENCES brand_certificates(id),
          CONSTRAINT chk_brand_certificate_images_file_size CHECK (file_size_bytes > 0),
          CONSTRAINT chk_brand_certificate_images_main CHECK (is_main IN (0, 1)),
          INDEX idx_brand_certificate_images_certificate_sort (certificate_id, sort_order)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
    )


def _ensure_client_request_id_support(connection: Connection) -> None:
    if not _has_table(connection, "request_logs"):
        return
    if not _has_column(connection, "request_logs", "client_request_id"):
        connection.exec_driver_sql(
            "ALTER TABLE request_logs ADD COLUMN client_request_id VARCHAR(128) NULL"
        )
    if not _has_index(connection, "request_logs", "idx_request_logs_client_request_id"):
        connection.exec_driver_sql(
            "CREATE INDEX idx_request_logs_client_request_id ON request_logs (client_request_id)"
        )


def _ensure_behavior_trace_support(connection: Connection) -> None:
    columns = {
        "request_logs": {
            "behavior_trace_id": "VARCHAR(128) NULL",
            "parent_behavior_event_id": "VARCHAR(128) NULL",
        },
        "usage_events": {
            "behavior_trace_id": "VARCHAR(128) NULL",
            "behavior_event_id": "VARCHAR(128) NULL",
        },
        "task_traces": {
            "behavior_trace_id": "VARCHAR(128) NULL",
        },
        "task_trace_spans": {
            "behavior_trace_id": "VARCHAR(128) NULL",
        },
    }
    indexes = {
        "request_logs": {
            "idx_request_logs_behavior_trace": "(behavior_trace_id, created_at)",
            "idx_request_logs_parent_behavior_event": "(parent_behavior_event_id, created_at)",
        },
        "usage_events": {
            "idx_usage_events_behavior_trace": "(behavior_trace_id, created_at)",
            "idx_usage_events_behavior_event": "(behavior_event_id)",
        },
        "task_traces": {
            "idx_task_traces_behavior_trace": "(behavior_trace_id, created_at)",
        },
        "task_trace_spans": {
            "idx_task_trace_spans_behavior_trace": "(behavior_trace_id, created_at)",
        },
    }
    for table_name, table_columns in columns.items():
        if not _has_table(connection, table_name):
            continue
        for column_name, column_definition in table_columns.items():
            if not _has_column(connection, table_name, column_name):
                connection.exec_driver_sql(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}")
        for index_name, column_spec in indexes.get(table_name, {}).items():
            if not _has_index(connection, table_name, index_name):
                connection.exec_driver_sql(f"CREATE INDEX {index_name} ON {table_name} {column_spec}")


def _ensure_log_query_indexes(connection: Connection) -> None:
    index_specs = {
        "request_logs": {
            "idx_request_logs_client_created": "(client_type, created_at)",
            "idx_request_logs_result_created": "(result, created_at)",
        },
        "usage_events": {
            "idx_usage_events_client_created": "(client_type, created_at)",
            "idx_usage_events_result_created": "(result, created_at)",
        },
        "audit_logs": {
            "idx_audit_logs_created": "(created_at)",
        },
    }
    for table_name, indexes in index_specs.items():
        if not _has_table(connection, table_name):
            continue
        for index_name, columns in indexes.items():
            if not _has_index(connection, table_name, index_name):
                connection.exec_driver_sql(f"CREATE INDEX {index_name} ON {table_name} {columns}")


def _ensure_task_trace_support(connection: Connection) -> None:
    for table_name in ("request_logs", "usage_events", "audit_logs"):
        if not _has_table(connection, table_name):
            continue
        if not _has_column(connection, table_name, "task_trace_id"):
            connection.exec_driver_sql(
                f"ALTER TABLE {table_name} ADD COLUMN task_trace_id VARCHAR(96) NULL"
            )
        if not _has_column(connection, table_name, "task_type"):
            connection.exec_driver_sql(
                f"ALTER TABLE {table_name} ADD COLUMN task_type VARCHAR(64) NULL"
            )
        index_name = f"idx_{table_name}_task_trace"
        if not _has_index(connection, table_name, index_name):
            connection.exec_driver_sql(
                f"CREATE INDEX {index_name} ON {table_name} (task_trace_id, created_at)"
            )

    _ensure_log_query_indexes(connection)

    if not _has_table(connection, "task_traces"):
        connection.exec_driver_sql(
            """
            CREATE TABLE task_traces (
              id CHAR(36) PRIMARY KEY,
              task_trace_id VARCHAR(96) NOT NULL UNIQUE,
              task_type VARCHAR(64) NOT NULL,
              status VARCHAR(32) NOT NULL,
              actor_user_id CHAR(36) NULL,
              client_type VARCHAR(32),
              parent_request_id VARCHAR(128),
              resource_type VARCHAR(64),
              resource_id VARCHAR(128),
              started_at VARCHAR(64) NOT NULL,
              ended_at VARCHAR(64),
              duration_ms INT NULL,
              slowest_span_name VARCHAR(96),
              error_code VARCHAR(64),
              summary VARCHAR(255) NOT NULL,
              metadata TEXT,
              created_at VARCHAR(64) NOT NULL,
              updated_at VARCHAR(64) NOT NULL,
              CONSTRAINT fk_task_traces_actor FOREIGN KEY(actor_user_id) REFERENCES users(id),
              CONSTRAINT chk_task_traces_status CHECK (status IN ('processing', 'success', 'failed', 'timeout', 'cancelled', 'skipped')),
              INDEX idx_task_traces_task_trace_id (task_trace_id),
              INDEX idx_task_traces_parent_request_id (parent_request_id, created_at),
              INDEX idx_task_traces_type_created (task_type, created_at),
              INDEX idx_task_traces_status_created (status, created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
        )
    else:
        if not _has_column(connection, "task_traces", "parent_request_id"):
            connection.exec_driver_sql(
                "ALTER TABLE task_traces ADD COLUMN parent_request_id VARCHAR(128) NULL"
            )
        if not _has_index(connection, "task_traces", "idx_task_traces_parent_request_id"):
            connection.exec_driver_sql(
                "CREATE INDEX idx_task_traces_parent_request_id ON task_traces (parent_request_id, created_at)"
            )

    if not _has_table(connection, "task_trace_spans"):
        connection.exec_driver_sql(
            """
            CREATE TABLE task_trace_spans (
              id CHAR(36) PRIMARY KEY,
              task_trace_id VARCHAR(96) NOT NULL,
              task_type VARCHAR(64) NOT NULL,
              span_name VARCHAR(96) NOT NULL,
              status VARCHAR(32) NOT NULL,
              started_at VARCHAR(64) NOT NULL,
              ended_at VARCHAR(64),
              duration_ms INT NULL,
              sequence INT NOT NULL DEFAULT 0,
              request_id VARCHAR(128),
              actor_user_id CHAR(36) NULL,
              client_type VARCHAR(32),
              resource_type VARCHAR(64),
              resource_id VARCHAR(128),
              error_code VARCHAR(64),
              summary VARCHAR(255) NOT NULL,
              metadata TEXT,
              created_at VARCHAR(64) NOT NULL,
              CONSTRAINT fk_task_trace_spans_actor FOREIGN KEY(actor_user_id) REFERENCES users(id),
              CONSTRAINT chk_task_trace_spans_status CHECK (status IN ('processing', 'success', 'failed', 'timeout', 'cancelled', 'skipped')),
              INDEX idx_task_trace_spans_trace_sequence (task_trace_id, sequence, started_at),
              INDEX idx_task_trace_spans_request_id (request_id),
              INDEX idx_task_trace_spans_type_created (task_type, created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
        )


def _ensure_banner_brand_id(connection: Connection) -> BannerBrandMigrationReport:
    if not _has_table(connection, "banners"):
        return BannerBrandMigrationReport(
            table_exists=False,
            columns_added=(),
            brand_id_added=False,
            status_position_index_added=False,
            sort_index_added=False,
            brand_index_added=False,
            topic_index_added=False,
            gallery_asset_index_added=False,
            brand_fk_added=False,
            topic_fk_added=False,
            gallery_asset_fk_added=False,
            check_constraints_rebuilt=(),
            brand_fk_skipped_dirty_rows=0,
            topic_fk_skipped_dirty_rows=0,
            gallery_asset_fk_skipped_dirty_rows=0,
        )

    columns_added: list[str] = []
    for column_name, column_definition in BANNER_WRITE_FIELD_COLUMNS.items():
        if not _has_column(connection, "banners", column_name):
            connection.exec_driver_sql(
                f"ALTER TABLE banners ADD COLUMN {column_name} {column_definition}"
            )
            columns_added.append(column_name)

    brand_id_added = "brand_id" in columns_added

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

    topic_index_added = False
    if _has_column(connection, "banners", "topic_id") and not _has_index(
        connection, "banners", BANNER_TOPIC_INDEX_NAME
    ):
        connection.exec_driver_sql(
            f"CREATE INDEX {BANNER_TOPIC_INDEX_NAME} ON banners (topic_id)"
        )
        topic_index_added = True

    gallery_asset_index_added = False
    if _has_column(connection, "banners", "sku_gallery_asset_id") and not _has_index(
        connection, "banners", BANNER_GALLERY_ASSET_INDEX_NAME
    ):
        connection.exec_driver_sql(
            f"CREATE INDEX {BANNER_GALLERY_ASSET_INDEX_NAME} ON banners (sku_gallery_asset_id)"
        )
        gallery_asset_index_added = True

    brand_fk_added = False
    brand_dirty_rows = 0
    if not _has_foreign_key(connection, "banners", BANNER_BRAND_FK_NAME):
        brand_dirty_rows = _dirty_banner_fk_rows(connection, "brand_id", "brands")
        if brand_dirty_rows == 0:
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
                brand_dirty_rows,
            )

    topic_fk_added = False
    topic_dirty_rows = 0
    if _has_column(connection, "banners", "topic_id") and not _has_foreign_key(
        connection, "banners", BANNER_TOPIC_FK_NAME
    ):
        topic_dirty_rows = _dirty_banner_fk_rows(connection, "topic_id", "topics")
        if topic_dirty_rows == 0:
            connection.exec_driver_sql(
                f"""
                ALTER TABLE banners
                ADD CONSTRAINT {BANNER_TOPIC_FK_NAME}
                FOREIGN KEY (topic_id) REFERENCES topics(id)
                """
            )
            topic_fk_added = True
        else:
            logger.warning(
                "Skipped %s because banners has %s row(s) referencing missing topics.",
                BANNER_TOPIC_FK_NAME,
                topic_dirty_rows,
            )

    gallery_asset_fk_added = False
    gallery_asset_dirty_rows = 0
    if _has_column(connection, "banners", "sku_gallery_asset_id") and not _has_foreign_key(
        connection, "banners", BANNER_GALLERY_ASSET_FK_NAME
    ):
        gallery_asset_dirty_rows = _dirty_banner_fk_rows(
            connection, "sku_gallery_asset_id", "tile_images"
        )
        if gallery_asset_dirty_rows == 0:
            connection.exec_driver_sql(
                f"""
                ALTER TABLE banners
                ADD CONSTRAINT {BANNER_GALLERY_ASSET_FK_NAME}
                FOREIGN KEY (sku_gallery_asset_id) REFERENCES tile_images(id)
                """
            )
            gallery_asset_fk_added = True
        else:
            logger.warning(
                "Skipped %s because banners has %s row(s) referencing missing tile images.",
                BANNER_GALLERY_ASSET_FK_NAME,
                gallery_asset_dirty_rows,
            )

    rebuilt_checks: list[str] = []
    for constraint_name, (check_clause, required_tokens) in BANNER_CHECK_CONSTRAINTS.items():
        existing_clause = _check_constraint_clause(connection, "banners", constraint_name)
        if existing_clause is not None and all(
            token in existing_clause for token in required_tokens
        ):
            continue
        if existing_clause is not None:
            connection.exec_driver_sql(f"ALTER TABLE banners DROP CHECK {constraint_name}")
        connection.exec_driver_sql(
            f"""
            ALTER TABLE banners
            ADD CONSTRAINT {constraint_name}
            CHECK ({check_clause})
            """
        )
        rebuilt_checks.append(constraint_name)

    report = BannerBrandMigrationReport(
        table_exists=True,
        columns_added=tuple(columns_added),
        brand_id_added=brand_id_added,
        status_position_index_added=status_position_index_added,
        sort_index_added=sort_index_added,
        brand_index_added=brand_index_added,
        topic_index_added=topic_index_added,
        gallery_asset_index_added=gallery_asset_index_added,
        brand_fk_added=brand_fk_added,
        topic_fk_added=topic_fk_added,
        gallery_asset_fk_added=gallery_asset_fk_added,
        check_constraints_rebuilt=tuple(rebuilt_checks),
        brand_fk_skipped_dirty_rows=brand_dirty_rows,
        topic_fk_skipped_dirty_rows=topic_dirty_rows,
        gallery_asset_fk_skipped_dirty_rows=gallery_asset_dirty_rows,
    )
    logger.info("MySQL banner compatibility migration report: %s", report)
    return report
