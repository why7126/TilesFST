"""Runtime effective settings: DB overrides merged with env/code defaults."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Callable

from app.core.config import settings
from app.repositories.system_settings_repository import SystemSettingsRepository

OBJECT_KEY_RULE_DESCRIPTION = (
    "{prefix}/{tenant}/{resource_type}/{uuid}.{ext} — 例：images/default/user/avatars/<uuid>.jpg"
)

AUDIT_SCOPE_DESCRIPTION = (
    "系统设置变更、账号敏感操作（创建/禁用/重置密码）、个人资料修改、媒体删除等"
)

NOTIFICATION_TEMPLATES: list[dict[str, str]] = [
    {
        "id": "account_freeze",
        "title": "账号冻结通知",
        "description": "账号被禁用或冻结时发送给账号持有人",
    },
    {
        "id": "sku_pending",
        "title": "SKU 待处理提醒",
        "description": "SKU 进入待完善或待发布状态时提醒运营",
    },
    {
        "id": "storage_capacity",
        "title": "存储容量预警",
        "description": "对象存储用量超过阈值时提醒管理员",
    },
]

SETTING_GROUPS: dict[str, list[str]] = {
    "basic": [
        "basic.platform_name",
        "basic.default_language",
        "basic.default_timezone",
        "basic.data_refresh_minutes",
        "basic.support_email",
        "basic.maintenance_window",
        "basic.system_announcement",
        "basic.show_dashboard_metrics",
        "basic.show_maintenance_notice",
    ],
    "security": [
        "security.password_min_length",
        "security.password_expiry_days",
        "security.require_uppercase",
        "security.require_lowercase",
        "security.require_digit",
        "security.require_special",
        "security.must_change_password_on_first_login",
        "security.login_lock_enabled",
        "security.login_failure_threshold",
        "security.login_lock_minutes",
        "security.jwt_access_token_expire_minutes",
    ],
    "media": [
        "media.max_image_size_mb",
        "media.max_video_size_mb",
        "media.allowed_image_types",
        "media.allowed_video_types",
    ],
    "notification": [
        "notification.account_freeze_notify",
        "notification.sku_pending_notify",
        "notification.storage_capacity_warn",
        "notification.storage_capacity_threshold_pct",
    ],
    "audit": [
        "audit.retention_days",
        "audit.allow_export",
        "audit.force_sensitive_audit",
        "audit.mask_sensitive_fields",
    ],
}

READONLY_FIELDS: dict[str, dict[str, Any]] = {
    "media": {
        "minio_bucket": settings.minio_bucket,
        "object_key_rule": OBJECT_KEY_RULE_DESCRIPTION,
    },
    "audit": {
        "scope_description": AUDIT_SCOPE_DESCRIPTION,
    },
    "notification": {
        "templates": NOTIFICATION_TEMPLATES,
    },
}


def _env_default(key: str) -> Any | None:
    mapping: dict[str, Callable[[], Any]] = {
        "media.max_image_size_mb": lambda: settings.max_image_size_mb,
        "media.max_video_size_mb": lambda: settings.max_video_size_mb,
        "media.allowed_image_types": lambda: settings.allowed_image_types,
        "media.allowed_video_types": lambda: settings.allowed_video_types,
        "security.jwt_access_token_expire_minutes": lambda: settings.jwt_access_token_expire_minutes,
    }
    factory = mapping.get(key)
    return factory() if factory else None


CODE_DEFAULTS: dict[str, Any] = {
    "basic.platform_name": "TILESFST",
    "basic.default_language": "zh-CN",
    "basic.default_timezone": "Asia/Shanghai",
    "basic.data_refresh_minutes": 15,
    "basic.support_email": "support@tilesfst.com",
    "basic.maintenance_window": "每周日 02:00-03:00",
    "basic.system_announcement": (
        "系统将在本周日 02:00-03:00 进行例行维护，请提前保存编辑内容。"
    ),
    "basic.show_dashboard_metrics": True,
    "basic.show_maintenance_notice": True,
    "security.password_min_length": 12,
    "security.password_expiry_days": 0,
    "security.require_uppercase": True,
    "security.require_lowercase": True,
    "security.require_digit": True,
    "security.require_special": True,
    "security.must_change_password_on_first_login": False,
    "security.login_lock_enabled": False,
    "security.login_failure_threshold": 5,
    "security.login_lock_minutes": 15,
    "notification.account_freeze_notify": True,
    "notification.sku_pending_notify": True,
    "notification.storage_capacity_warn": True,
    "notification.storage_capacity_threshold_pct": 80,
    "audit.retention_days": 365,
    "audit.allow_export": True,
    "audit.force_sensitive_audit": True,
    "audit.mask_sensitive_fields": True,
}


@dataclass(frozen=True)
class PasswordPolicy:
    min_length: int = 12
    max_length: int = 32
    require_uppercase: bool = True
    require_lowercase: bool = True
    require_digit: bool = True
    require_special: bool = True


class EffectiveSettingsService:
    def __init__(self, repo: SystemSettingsRepository) -> None:
        self._repo = repo

    def get_effective(self, key: str) -> Any:
        record = self._repo.get(key)
        if record is not None:
            return self._deserialize(record.value)
        env_val = _env_default(key)
        if env_val is not None:
            return env_val
        return CODE_DEFAULTS.get(key)

    def get_group_keys(self, group: str) -> list[str]:
        return list(SETTING_GROUPS.get(group, []))

    def get_group_effective(self, group: str) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key in self.get_group_keys(group):
            short_key = key.split(".", 1)[1]
            result[short_key] = self.get_effective(key)
        readonly = READONLY_FIELDS.get(group)
        if readonly:
            result.update(readonly)
        return result

    def get_password_policy(self) -> PasswordPolicy:
        return PasswordPolicy(
            min_length=int(self.get_effective("security.password_min_length")),
            require_uppercase=bool(self.get_effective("security.require_uppercase")),
            require_lowercase=bool(self.get_effective("security.require_lowercase")),
            require_digit=bool(self.get_effective("security.require_digit")),
            require_special=bool(self.get_effective("security.require_special")),
        )

    def get_jwt_access_expire_minutes(self) -> int:
        return int(self.get_effective("security.jwt_access_token_expire_minutes"))

    def max_image_size_mb(self) -> int:
        return int(self.get_effective("media.max_image_size_mb"))

    def max_video_size_mb(self) -> int:
        return int(self.get_effective("media.max_video_size_mb"))

    def allowed_image_type_set(self) -> frozenset[str]:
        raw = str(self.get_effective("media.allowed_image_types"))
        return frozenset(part.strip() for part in raw.split(",") if part.strip())

    def allowed_video_type_set(self) -> frozenset[str]:
        raw = str(self.get_effective("media.allowed_video_types"))
        return frozenset(part.strip() for part in raw.split(",") if part.strip())

    @staticmethod
    def serialize_value(value: Any) -> str:
        if isinstance(value, bool):
            return json.dumps(value)
        if isinstance(value, (int, float)):
            return json.dumps(value)
        if isinstance(value, str):
            return value
        return json.dumps(value)

    @staticmethod
    def _deserialize(raw: str) -> Any:
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return raw
