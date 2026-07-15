"""Brand certificate persistence."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


@dataclass
class BrandCertificateRecord:
    id: int
    brand_id: int
    brand_name: str
    name: str
    sort_order: int
    type: str
    certificate_no: str | None
    issuer: str | None
    file_url: str
    file_key: str
    file_name: str
    file_mime_type: str
    file_size_bytes: int
    is_permanent: bool
    effective_date: str | None
    expiry_date: str | None
    is_visible: bool
    remark: str | None
    deleted_at: str | None
    created_at: str
    updated_at: str


@dataclass
class BrandCertificateListResult:
    items: list[BrandCertificateRecord]
    total: int
    summary_rows: list[BrandCertificateRecord]


class BrandCertificateRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    @staticmethod
    def _to_record(row: dict[str, Any]) -> BrandCertificateRecord:
        return BrandCertificateRecord(
            id=int(row["id"]),
            brand_id=int(row["brand_id"]),
            brand_name=row["brand_name"],
            name=row["name"],
            sort_order=int(row["sort_order"]),
            type=row["type"],
            certificate_no=row.get("certificate_no"),
            issuer=row.get("issuer"),
            file_url=row["file_url"],
            file_key=row["file_key"],
            file_name=row["file_name"],
            file_mime_type=row["file_mime_type"],
            file_size_bytes=int(row["file_size_bytes"]),
            is_permanent=bool(row["is_permanent"]),
            effective_date=row.get("effective_date"),
            expiry_date=row.get("expiry_date"),
            is_visible=bool(row["is_visible"]),
            remark=row.get("remark"),
            deleted_at=row.get("deleted_at"),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def list_certificates(
        self,
        *,
        page: int,
        page_size: int,
        keyword: str | None,
        brand_id: int | None,
        certificate_type: str | None,
        display_status: str | None,
    ) -> BrandCertificateListResult:
        conditions = ["bc.deleted_at IS NULL"]
        params: dict[str, Any] = {}

        if keyword:
            conditions.append(
                "(bc.name LIKE :keyword OR bc.certificate_no LIKE :keyword OR bc.issuer LIKE :keyword)"
            )
            params["keyword"] = f"%{keyword}%"
        if brand_id:
            conditions.append("bc.brand_id = :brand_id")
            params["brand_id"] = brand_id
        if certificate_type:
            conditions.append("bc.type = :type")
            params["type"] = certificate_type
        if display_status == "VISIBLE":
            conditions.append("bc.is_visible = 1")
        elif display_status == "HIDDEN":
            conditions.append("bc.is_visible = 0")

        where_sql = " AND ".join(conditions)
        base_select = f"""
            SELECT bc.*, b.name AS brand_name
            FROM brand_certificates bc
            JOIN brands b ON b.id = bc.brand_id
            WHERE {where_sql}
        """
        total = int(
            self._db.execute(text(f"SELECT COUNT(*) FROM ({base_select}) scoped"), params)
            .scalar_one()
            or 0
        )
        offset = (page - 1) * page_size
        rows = (
            self._db.execute(
                text(
                    f"""
                    {base_select}
                    ORDER BY bc.sort_order ASC, bc.updated_at DESC, bc.id DESC
                    LIMIT :limit OFFSET :offset
                    """
                ),
                {**params, "limit": page_size, "offset": offset},
            )
            .mappings()
            .all()
        )
        summary_rows = (
            self._db.execute(
                text(
                    """
                    SELECT bc.*, b.name AS brand_name
                    FROM brand_certificates bc
                    JOIN brands b ON b.id = bc.brand_id
                    WHERE bc.deleted_at IS NULL
                    """
                )
            )
            .mappings()
            .all()
        )
        return BrandCertificateListResult(
            items=[self._to_record(dict(row)) for row in rows],
            total=total,
            summary_rows=[self._to_record(dict(row)) for row in summary_rows],
        )

    def get_by_id(self, certificate_id: int) -> BrandCertificateRecord | None:
        row = (
            self._db.execute(
                text(
                    """
                    SELECT bc.*, b.name AS brand_name
                    FROM brand_certificates bc
                    JOIN brands b ON b.id = bc.brand_id
                    WHERE bc.id = :id AND bc.deleted_at IS NULL
                    """
                ),
                {"id": certificate_id},
            )
            .mappings()
            .first()
        )
        return self._to_record(dict(row)) if row else None

    def get_by_brand_and_name(
        self,
        *,
        brand_id: int,
        name: str,
        exclude_id: int | None = None,
    ) -> BrandCertificateRecord | None:
        sql = """
            SELECT bc.*, b.name AS brand_name
            FROM brand_certificates bc
            JOIN brands b ON b.id = bc.brand_id
            WHERE bc.brand_id = :brand_id
              AND bc.name = :name
              AND bc.deleted_at IS NULL
        """
        params: dict[str, Any] = {"brand_id": brand_id, "name": name}
        if exclude_id is not None:
            sql += " AND bc.id != :exclude_id"
            params["exclude_id"] = exclude_id
        row = self._db.execute(text(sql), params).mappings().first()
        return self._to_record(dict(row)) if row else None

    def count_active_by_brand(self, brand_id: int) -> int:
        return int(
            self._db.execute(
                text(
                    """
                    SELECT COUNT(*) FROM brand_certificates
                    WHERE brand_id = :brand_id AND deleted_at IS NULL
                    """
                ),
                {"brand_id": brand_id},
            ).scalar_one()
            or 0
        )

    def create(self, values: dict[str, Any]) -> BrandCertificateRecord:
        now = datetime.now(UTC).isoformat()
        cursor = self._db.execute(
            text(
                """
                INSERT INTO brand_certificates (
                  brand_id, name, sort_order, type, certificate_no, issuer,
                  file_url, file_key, file_name, file_mime_type, file_size_bytes,
                  is_permanent, effective_date, expiry_date, is_visible, remark,
                  deleted_at, created_at, updated_at
                ) VALUES (
                  :brand_id, :name, :sort_order, :type, :certificate_no, :issuer,
                  :file_url, :file_key, :file_name, :file_mime_type, :file_size_bytes,
                  :is_permanent, :effective_date, :expiry_date, :is_visible, :remark,
                  NULL, :created_at, :updated_at
                )
                """
            ),
            {**values, "created_at": now, "updated_at": now},
        )
        self._db.commit()
        record = self.get_by_id(int(cursor.lastrowid))
        assert record is not None
        return record

    def update(self, certificate_id: int, values: dict[str, Any]) -> BrandCertificateRecord | None:
        now = datetime.now(UTC).isoformat()
        self._db.execute(
            text(
                """
                UPDATE brand_certificates SET
                  brand_id = :brand_id,
                  name = :name,
                  sort_order = :sort_order,
                  type = :type,
                  certificate_no = :certificate_no,
                  issuer = :issuer,
                  file_url = :file_url,
                  file_key = :file_key,
                  file_name = :file_name,
                  file_mime_type = :file_mime_type,
                  file_size_bytes = :file_size_bytes,
                  is_permanent = :is_permanent,
                  effective_date = :effective_date,
                  expiry_date = :expiry_date,
                  is_visible = :is_visible,
                  remark = :remark,
                  updated_at = :updated_at
                WHERE id = :id AND deleted_at IS NULL
                """
            ),
            {**values, "id": certificate_id, "updated_at": now},
        )
        self._db.commit()
        return self.get_by_id(certificate_id)

    def set_visibility(self, certificate_id: int, is_visible: bool) -> BrandCertificateRecord | None:
        now = datetime.now(UTC).isoformat()
        self._db.execute(
            text(
                """
                UPDATE brand_certificates
                SET is_visible = :is_visible, updated_at = :updated_at
                WHERE id = :id AND deleted_at IS NULL
                """
            ),
            {"id": certificate_id, "is_visible": int(is_visible), "updated_at": now},
        )
        self._db.commit()
        return self.get_by_id(certificate_id)

    def soft_delete(self, certificate_id: int) -> bool:
        now = datetime.now(UTC).isoformat()
        result = self._db.execute(
            text(
                """
                UPDATE brand_certificates
                SET deleted_at = :deleted_at, updated_at = :updated_at
                WHERE id = :id AND deleted_at IS NULL
                """
            ),
            {"id": certificate_id, "deleted_at": now, "updated_at": now},
        )
        self._db.commit()
        return result.rowcount > 0
