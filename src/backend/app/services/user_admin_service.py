"""Admin user management business logic."""

from __future__ import annotations

from app.core.exceptions import (
    UserCannotDeleteLoggedInError,
    UserInvalidStatusTransitionError,
    UserInvalidUsernameError,
    UserNotFoundError,
    UserUsernameTakenError,
)
from app.core.user_validation import generate_random_password, validate_username
from app.repositories.user_repository import UserRecord, UserRepository
from app.schemas.user_admin import (
    UserAdminItem,
    UserAdminListData,
    UserAdminSummary,
    UserCreateData,
    UserCreateRequest,
    UserUpdateRequest,
)

VALID_ROLES = frozenset({"admin", "employee", "store_owner"})
VALID_STATUSES = frozenset({"active", "disabled", "deleted"})


class UserAdminService:
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    @staticmethod
    def to_item(user: UserRecord) -> UserAdminItem:
        return UserAdminItem(
            id=user.id,
            username=user.username,
            display_name=user.display_name,
            role=user.role,
            status=user.status,
            avatar_object_key=user.avatar_object_key,
            email=user.email,
            phone=user.phone,
            last_login_at=user.last_login_at,
            created_at=user.created_at,
        )

    def list_users(
        self,
        *,
        page: int,
        page_size: int,
        keyword: str | None,
        role: str | None,
        status: str | None,
        login_filter: str | None,
    ) -> UserAdminListData:
        if page_size not in {10, 20, 50}:
            page_size = 10
        if page < 1:
            page = 1

        result = self._repo.list_users(
            page=page,
            page_size=page_size,
            keyword=keyword,
            role=role,
            status=status,
            login_filter=login_filter,
        )
        return UserAdminListData(
            items=[self.to_item(user) for user in result.items],
            page=page,
            page_size=page_size,
            total=result.total,
            summary=UserAdminSummary(
                total=result.summary["total"],
                filtered=result.summary["filtered"],
                active_count=result.summary["active_count"],
                disabled_count=result.summary["disabled_count"],
            ),
        )

    def get_user(self, user_id: str) -> UserAdminItem:
        user = self._repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError()
        return self.to_item(user)

    def create_user(self, payload: UserCreateRequest) -> UserCreateData:
        username = payload.username.strip().lower()
        error = validate_username(username)
        if error:
            raise UserInvalidUsernameError(error)
        if payload.role not in VALID_ROLES:
            raise UserInvalidUsernameError("无效的角色")
        if self._repo.get_by_username(username):
            raise UserUsernameTakenError()

        password = generate_random_password()
        user = self._repo.create_user(
            username=username,
            password=password,
            display_name=payload.display_name.strip() if payload.display_name else None,
            role=payload.role,
            avatar_object_key=payload.avatar_object_key,
        )
        return UserCreateData(user=self.to_item(user), initial_password=password)

    def update_user(self, user_id: str, payload: UserUpdateRequest) -> UserAdminItem:
        user = self._repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError()
        if user.status == "deleted":
            raise UserInvalidStatusTransitionError("已删除用户不可编辑")
        if payload.role is not None and payload.role not in VALID_ROLES:
            raise UserInvalidUsernameError("无效的角色")

        display_name = payload.display_name
        if display_name is not None:
            display_name = display_name.strip() or None

        updated = self._repo.update_user(
            user_id,
            display_name=display_name if payload.display_name is not None else None,
            role=payload.role,
            avatar_object_key=payload.avatar_object_key,
            update_avatar=payload.avatar_object_key is not None,
        )
        assert updated is not None
        return self.to_item(updated)

    def reset_password(self, user_id: str) -> str:
        user = self._repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError()
        if user.status == "deleted":
            raise UserInvalidStatusTransitionError("已删除用户不可重置密码")

        password = generate_random_password()
        self._repo.update_password(user_id, password)
        return password

    def update_status(self, user_id: str, status: str) -> UserAdminItem:
        if status not in VALID_STATUSES:
            raise UserInvalidStatusTransitionError()

        user = self._repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError()

        if status == "deleted":
            if user.last_login_at is not None:
                raise UserCannotDeleteLoggedInError()
        elif user.status == "deleted":
            raise UserInvalidStatusTransitionError("已删除用户不可变更状态")

        updated = self._repo.update_status(user_id, status)
        assert updated is not None
        return self.to_item(updated)
