"""Pydantic schemas for system settings API."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class BasicSettingsPatch(BaseModel):
    platform_name: str | None = None
    default_language: str | None = None
    default_timezone: str | None = None
    data_refresh_minutes: int | None = None
    support_email: str | None = None
    maintenance_window: str | None = None
    system_announcement: str | None = None
    show_dashboard_metrics: bool | None = None
    show_maintenance_notice: bool | None = None


class MediaSettingsPatch(BaseModel):
    max_image_size_mb: int | None = None
    max_video_size_mb: int | None = None
    max_file_size_mb: int | None = None
    allowed_image_types: str | None = None
    allowed_video_types: str | None = None


class SecuritySettingsPatch(BaseModel):
    password_min_length: int | None = None
    password_expiry_days: int | None = None
    require_uppercase: bool | None = None
    require_lowercase: bool | None = None
    require_digit: bool | None = None
    require_special: bool | None = None
    must_change_password_on_first_login: bool | None = None
    login_lock_enabled: bool | None = None
    login_failure_threshold: int | None = None
    login_lock_minutes: int | None = None
    jwt_access_token_expire_minutes: int | None = None


class NotificationSettingsPatch(BaseModel):
    account_freeze_notify: bool | None = None
    sku_pending_notify: bool | None = None
    storage_capacity_warn: bool | None = None
    storage_capacity_threshold_pct: int | None = None


class AuditSettingsPatch(BaseModel):
    retention_days: int | None = None
    allow_export: bool | None = None
    force_sensitive_audit: bool | None = None
    mask_sensitive_fields: bool | None = None


class NotificationTemplateItem(BaseModel):
    id: str
    title: str
    description: str


class BasicSettingsData(BaseModel):
    model_config = ConfigDict(extra="allow")

    platform_name: str
    default_language: str
    default_timezone: str
    data_refresh_minutes: int
    support_email: str
    maintenance_window: str
    system_announcement: str
    show_dashboard_metrics: bool
    show_maintenance_notice: bool


class MediaSettingsData(BaseModel):
    model_config = ConfigDict(extra="allow")

    max_image_size_mb: int
    max_video_size_mb: int
    max_file_size_mb: int
    allowed_image_types: str
    allowed_video_types: str
    minio_bucket: str
    object_key_rule: str


class SecuritySettingsData(BaseModel):
    model_config = ConfigDict(extra="allow")

    password_min_length: int
    password_expiry_days: int
    require_uppercase: bool
    require_lowercase: bool
    require_digit: bool
    require_special: bool
    must_change_password_on_first_login: bool
    login_lock_enabled: bool
    login_failure_threshold: int
    login_lock_minutes: int
    jwt_access_token_expire_minutes: int


class NotificationSettingsData(BaseModel):
    model_config = ConfigDict(extra="allow")

    account_freeze_notify: bool
    sku_pending_notify: bool
    storage_capacity_warn: bool
    storage_capacity_threshold_pct: int
    templates: list[NotificationTemplateItem]


class AuditSettingsData(BaseModel):
    model_config = ConfigDict(extra="allow")

    retention_days: int
    allow_export: bool
    force_sensitive_audit: bool
    mask_sensitive_fields: bool
    scope_description: str


class SystemSettingsAuditItem(BaseModel):
    id: str
    actor_user_id: str | None = None
    actor_display_name: str | None = None
    action_type: str
    summary: str
    created_at: str


class SystemSettingsAuditRecentData(BaseModel):
    items: list[SystemSettingsAuditItem]


class SystemSettingsGroupResponse(BaseModel):
    group: str
    data: dict[str, Any] = Field(default_factory=dict)
