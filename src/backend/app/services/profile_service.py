"""Profile self-service business logic."""

from __future__ import annotations

import re

from app.core.exceptions import ProfileValidationError
from app.repositories.profile_activity_repository import ProfileActivityRepository
from app.repositories.user_repository import UserRecord, UserRepository
from app.schemas.profile import ProfileActivityItem, ProfileMe, ProfilePatchRequest

_EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
_PHONE_RE = re.compile(r"^[\d\s+\-()]{6,32}$")

_ACTION_LABELS = {
    "profile_update": "资料更新",
    "avatar_update": "头像更新",
    "login": "登录后台",
}


def _avatar_url(object_key: str | None) -> str | None:
    if not object_key:
        return None
    return f"/media/{object_key}"


def _role_label(role: str) -> str:
    labels = {
        "admin": "后台管理员",
        "employee": "后台运营",
        "store_owner": "前台用户",
    }
    return labels.get(role, role)


def _status_label(status: str) -> str:
    labels = {
        "active": "正常",
        "disabled": "已冻结",
        "deleted": "已删除",
    }
    return labels.get(status, status)


class ProfileService:
    def __init__(
        self,
        user_repo: UserRepository,
        activity_repo: ProfileActivityRepository,
    ) -> None:
        self._users = user_repo
        self._activities = activity_repo

    @staticmethod
    def to_profile(user: UserRecord) -> ProfileMe:
        display_name = (user.display_name or user.username).strip()
        return ProfileMe(
            id=user.id,
            username=user.username,
            display_name=display_name,
            role=user.role,
            status=user.status,
            email=user.email,
            phone=user.phone,
            remark=user.remark,
            avatar_object_key=user.avatar_object_key,
            avatar_url=_avatar_url(user.avatar_object_key),
            last_login_at=user.last_login_at,
            updated_at=user.updated_at,
        )

    def get_me(self, user: UserRecord) -> ProfileMe:
        return self.to_profile(user)

    def list_activities(self, user: UserRecord) -> list[ProfileActivityItem]:
        records = self._activities.list_by_user(user.id, limit=5)
        return [
            ProfileActivityItem(
                id=record.id,
                action_type=record.action_type,
                summary=record.summary,
                created_at=record.created_at,
            )
            for record in records
        ]

    def patch_me(self, user: UserRecord, payload: ProfilePatchRequest) -> ProfileMe:
        fields_set = payload.model_fields_set
        if not fields_set:
            raise ProfileValidationError("请至少提供一个可更新字段")

        current = self.to_profile(user)
        display_name = payload.display_name if "display_name" in fields_set else current.display_name
        email = payload.email if "email" in fields_set else current.email
        phone = payload.phone if "phone" in fields_set else current.phone
        remark = payload.remark if "remark" in fields_set else current.remark
        avatar_object_key = (
            payload.avatar_object_key
            if "avatar_object_key" in fields_set
            else current.avatar_object_key
        )

        self._validate_profile_fields(
            display_name=display_name,
            email=email,
            phone=phone,
            remark=remark,
        )

        avatar_changed = (
            "avatar_object_key" in fields_set
            and avatar_object_key != user.avatar_object_key
        )
        profile_changed = any(
            [
                "display_name" in fields_set and display_name != current.display_name,
                "email" in fields_set and email != current.email,
                "phone" in fields_set and phone != current.phone,
                "remark" in fields_set and remark != current.remark,
            ]
        )

        updated = self._users.update_profile(
            user.id,
            display_name=display_name,
            email=email,
            phone=phone,
            remark=remark,
            avatar_object_key=avatar_object_key,
        )
        if updated is None:
            raise ProfileValidationError("用户不存在")

        if avatar_changed:
            self._activities.insert(
                user_id=user.id,
                action_type="avatar_update",
                summary="上传新头像",
            )

        if profile_changed:
            summary = self._build_profile_update_summary(
                user=user,
                payload=payload,
                current=current,
            )
            self._activities.insert(
                user_id=user.id,
                action_type="profile_update",
                summary=summary,
            )

        return self.to_profile(updated)

    @staticmethod
    def _validate_profile_fields(
        *,
        display_name: str,
        email: str | None,
        phone: str | None,
        remark: str | None,
    ) -> None:
        name = display_name.strip()
        if len(name) < 2 or len(name) > 32:
            raise ProfileValidationError("昵称长度须为 2–32 个字符")

        if email is not None and email.strip():
            if not _EMAIL_RE.match(email.strip()):
                raise ProfileValidationError("联系邮箱格式无效")

        if phone is not None and phone.strip():
            if not _PHONE_RE.match(phone.strip()):
                raise ProfileValidationError("手机号码格式无效")

        if remark is not None and len(remark) > 200:
            raise ProfileValidationError("备注说明不能超过 200 字")

    @staticmethod
    def _build_profile_update_summary(
        *,
        user: UserRecord,
        payload: ProfilePatchRequest,
        current: ProfileMe,
    ) -> str:
        fields_set = payload.model_fields_set
        parts: list[str] = []
        if "display_name" in fields_set and payload.display_name != current.display_name:
            parts.append("昵称")
        if "email" in fields_set and payload.email != current.email:
            parts.append("邮箱")
        if "phone" in fields_set and payload.phone != current.phone:
            parts.append("手机")
        if "remark" in fields_set and payload.remark != current.remark:
            parts.append("备注")
        if not parts:
            return "更新资料"
        return f"修改{'与'.join(parts)}"


def activity_title(action_type: str) -> str:
    return _ACTION_LABELS.get(action_type, action_type)


def profile_role_label(role: str) -> str:
    return _role_label(role)


def profile_status_label(status: str) -> str:
    return _status_label(status)
