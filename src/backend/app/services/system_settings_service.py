"""System settings group read/update/reset business logic."""

from __future__ import annotations

import json
import re
from typing import Any

from app.core.exceptions import AppError
from app.repositories.audit_log_repository import AuditLogRepository
from app.repositories.system_settings_repository import SystemSettingsRepository
from app.services.effective_settings_service import (
    CODE_DEFAULTS,
    EffectiveSettingsService,
    SETTING_GROUPS,
    _env_default,
)

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
VALID_GROUPS = frozenset(SETTING_GROUPS.keys())


class SystemSettingsService:
    def __init__(
        self,
        settings_repo: SystemSettingsRepository,
        audit_repo: AuditLogRepository,
    ) -> None:
        self._settings_repo = settings_repo
        self._audit_repo = audit_repo
        self._effective = EffectiveSettingsService(settings_repo)

    def get_group(self, group: str) -> dict[str, Any]:
        self._assert_valid_group(group)
        return self._effective.get_group_effective(group)

    def patch_group(
        self,
        group: str,
        payload: dict[str, Any],
        actor_user_id: str,
    ) -> dict[str, Any]:
        self._assert_valid_group(group)
        allowed_short_keys = {k.split(".", 1)[1] for k in SETTING_GROUPS[group]}
        changes: dict[str, Any] = {}
        for short_key, value in payload.items():
            if short_key not in allowed_short_keys:
                continue
            full_key = f"{group}.{short_key}"
            validated = self._validate_field(group, short_key, value)
            serialized = EffectiveSettingsService.serialize_value(validated)
            self._settings_repo.set(full_key, serialized, actor_user_id)
            changes[short_key] = validated

        if changes:
            summary = f"更新 {group} 分组配置：{', '.join(sorted(changes.keys()))}"
            self._audit_repo.insert(
                actor_user_id=actor_user_id,
                domain="system_settings",
                action_type="settings_update",
                summary=summary,
                metadata=json.dumps({"group": group, "changes": changes}, ensure_ascii=False),
            )

        return self.get_group(group)

    def reset_group(self, group: str, actor_user_id: str) -> dict[str, Any]:
        self._assert_valid_group(group)
        prefix = f"{group}."
        deleted = self._settings_repo.delete_by_prefix(prefix)
        summary = f"恢复 {group} 分组默认配置（清除 {deleted} 项覆盖）"
        self._audit_repo.insert(
            actor_user_id=actor_user_id,
            domain="system_settings",
            action_type="settings_reset",
            summary=summary,
            metadata=json.dumps({"group": group, "deleted_count": deleted}, ensure_ascii=False),
        )
        return self.get_group(group)

    def list_recent_audit(self, limit: int = 10) -> list[dict[str, Any]]:
        records = self._audit_repo.list_recent_by_domain("system_settings", limit=limit)
        return [
            {
                "id": record.id,
                "actor_user_id": record.actor_user_id,
                "actor_display_name": record.actor_display_name,
                "action_type": record.action_type,
                "summary": record.summary,
                "created_at": record.created_at,
            }
            for record in records
        ]

    def _assert_valid_group(self, group: str) -> None:
        if group not in VALID_GROUPS:
            raise AppError(status_code=404, code=40400, message="未知的设置分组")

    def _validate_field(self, group: str, short_key: str, value: Any) -> Any:
        if group == "basic":
            return self._validate_basic(short_key, value)
        if group == "media":
            return self._validate_media(short_key, value)
        if group == "security":
            return self._validate_security(short_key, value)
        if group == "notification":
            return self._validate_notification(short_key, value)
        if group == "audit":
            return self._validate_audit(short_key, value)
        return value

    def _validate_basic(self, short_key: str, value: Any) -> Any:
        if short_key == "platform_name":
            text = str(value).strip()
            if len(text) < 2 or len(text) > 64:
                raise AppError(status_code=400, code=40000, message="平台名称须为 2–64 字")
            return text
        if short_key == "default_language":
            lang = str(value).strip()
            if lang not in {"zh-CN", "en"}:
                raise AppError(status_code=400, code=40000, message="默认语言无效")
            return lang
        if short_key == "default_timezone":
            tz = str(value).strip()
            if not tz:
                raise AppError(status_code=400, code=40000, message="默认时区无效")
            return tz
        if short_key == "data_refresh_minutes":
            minutes = int(value)
            if minutes < 1 or minutes > 1440:
                raise AppError(status_code=400, code=40000, message="数据刷新周期须为 1–1440 分钟")
            return minutes
        if short_key == "support_email":
            email = str(value).strip()
            if email and not EMAIL_PATTERN.match(email):
                raise AppError(status_code=400, code=40000, message="客服邮箱格式无效")
            return email
        if short_key == "maintenance_window":
            return str(value).strip()
        if short_key == "system_announcement":
            text = str(value)
            if len(text) > 500:
                raise AppError(status_code=400, code=40000, message="系统公告不能超过 500 字")
            return text
        if short_key in {"show_dashboard_metrics", "show_maintenance_notice"}:
            return bool(value)
        return value

    def _validate_media(self, short_key: str, value: Any) -> Any:
        if short_key == "max_image_size_mb":
            size = int(value)
            if size < 1 or size > 100:
                raise AppError(status_code=400, code=40000, message="图片最大尺寸须为 1–100 MB")
            return size
        if short_key == "max_video_size_mb":
            size = int(value)
            if size < 1 or size > 2000:
                raise AppError(status_code=400, code=40000, message="视频最大尺寸须为 1–2000 MB")
            return size
        if short_key == "allowed_image_types":
            types = self._normalize_mime_list(str(value))
            env_default = str(_env_default("media.allowed_image_types") or "")
            allowed_subset = frozenset(
                part.strip() for part in env_default.split(",") if part.strip()
            ) or frozenset(
                {
                    "image/jpeg",
                    "image/jpg",
                    "image/png",
                    "image/webp",
                    "image/gif",
                    "image/svg+xml",
                    "image/bmp",
                    "image/tiff",
                    "image/heic",
                }
            )
            if not types or not set(types).issubset(allowed_subset):
                raise AppError(status_code=400, code=40000, message="图片 MIME 列表无效")
            return ",".join(types)
        if short_key == "allowed_video_types":
            types = self._normalize_mime_list(str(value))
            env_default = str(_env_default("media.allowed_video_types") or "")
            allowed_subset = frozenset(
                part.strip() for part in env_default.split(",") if part.strip()
            ) or frozenset(
                {
                    "video/mp4",
                    "video/quicktime",
                    "video/x-msvideo",
                    "video/webm",
                    "video/x-matroska",
                    "video/mpeg",
                    "video/3gpp",
                }
            )
            if not types or not set(types).issubset(allowed_subset):
                raise AppError(status_code=400, code=40000, message="视频 MIME 列表无效")
            return ",".join(types)
        return value

    def _validate_security(self, short_key: str, value: Any) -> Any:
        if short_key == "password_min_length":
            length = int(value)
            if length < 8 or length > 32:
                raise AppError(status_code=400, code=40000, message="密码最小长度须为 8–32")
            return length
        if short_key == "password_expiry_days":
            days = int(value)
            if days < 0 or days > 3650:
                raise AppError(status_code=400, code=40000, message="密码有效期天数无效")
            return days
        if short_key in {
            "require_uppercase",
            "require_lowercase",
            "require_digit",
            "require_special",
            "must_change_password_on_first_login",
            "login_lock_enabled",
        }:
            return bool(value)
        if short_key == "login_failure_threshold":
            threshold = int(value)
            if threshold < 3 or threshold > 20:
                raise AppError(status_code=400, code=40000, message="登录失败阈值须为 3–20")
            return threshold
        if short_key == "login_lock_minutes":
            minutes = int(value)
            if minutes < 5 or minutes > 1440:
                raise AppError(status_code=400, code=40000, message="锁定时长须为 5–1440 分钟")
            return minutes
        if short_key == "jwt_access_token_expire_minutes":
            minutes = int(value)
            if minutes < 15 or minutes > 1440:
                raise AppError(status_code=400, code=40000, message="会话超时须为 15–1440 分钟")
            return minutes
        return value

    def _validate_notification(self, short_key: str, value: Any) -> Any:
        if short_key in {
            "account_freeze_notify",
            "sku_pending_notify",
            "storage_capacity_warn",
        }:
            return bool(value)
        if short_key == "storage_capacity_threshold_pct":
            pct = int(value)
            if pct < 50 or pct > 95:
                raise AppError(status_code=400, code=40000, message="容量预警阈值须为 50–95%")
            return pct
        return value

    def _validate_audit(self, short_key: str, value: Any) -> Any:
        if short_key == "retention_days":
            days = int(value)
            if days < 30 or days > 3650:
                raise AppError(status_code=400, code=40000, message="日志保留天数须为 30–3650")
            return days
        if short_key in {"allow_export", "force_sensitive_audit", "mask_sensitive_fields"}:
            return bool(value)
        return value

    @staticmethod
    def _normalize_mime_list(raw: str) -> list[str]:
        return [part.strip() for part in raw.split(",") if part.strip()]

    @staticmethod
    def get_default_value(full_key: str) -> Any:
        env_val = _env_default(full_key)
        if env_val is not None:
            return env_val
        return CODE_DEFAULTS.get(full_key)
