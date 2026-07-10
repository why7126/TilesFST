"""Shared API exceptions."""

from __future__ import annotations

from typing import Any


class AppError(Exception):
    def __init__(
        self,
        *,
        status_code: int,
        code: int,
        message: str,
        data: dict[str, Any] | None = None,
    ) -> None:
        self.status_code = status_code
        self.code = code
        self.message = message
        self.data = data
        super().__init__(message)


class AuthInvalidRequestError(AppError):
    def __init__(self, message: str = "请求参数无效") -> None:
        super().__init__(status_code=400, code=40001, message=message)


class AuthInvalidCredentialsError(AppError):
    def __init__(self, message: str = "账号或密码错误") -> None:
        super().__init__(status_code=401, code=40101, message=message)


class AuthUserDisabledError(AppError):
    def __init__(self, message: str = "账号已停用，请联系管理员") -> None:
        super().__init__(status_code=403, code=40301, message=message)


class AuthUnauthorizedError(AppError):
    def __init__(self, message: str = "未登录或登录已过期") -> None:
        super().__init__(status_code=401, code=40102, message=message)


class AuthForbiddenError(AppError):
    def __init__(self, message: str = "无权限访问") -> None:
        super().__init__(status_code=403, code=40302, message=message)


class UserInvalidUsernameError(AppError):
    def __init__(self, message: str = "用户名格式无效") -> None:
        super().__init__(status_code=400, code=40010, message=message)


class UserUsernameTakenError(AppError):
    def __init__(self, message: str = "用户名已存在") -> None:
        super().__init__(status_code=409, code=40910, message=message)


class UserNotFoundError(AppError):
    def __init__(self, message: str = "用户不存在") -> None:
        super().__init__(status_code=404, code=40410, message=message)


class UserCannotDeleteLoggedInError(AppError):
    def __init__(self, message: str = "已登录过的用户不允许删除") -> None:
        super().__init__(status_code=400, code=40011, message=message)


class UserInvalidStatusTransitionError(AppError):
    def __init__(self, message: str = "无效的状态变更") -> None:
        super().__init__(status_code=400, code=40012, message=message)


class UserProtectedAccountError(AppError):
    def __init__(self, message: str = "系统保底管理员账号不允许执行该操作") -> None:
        from app.core.error_codes import USER_PROTECTED_ACCOUNT

        super().__init__(status_code=403, code=USER_PROTECTED_ACCOUNT, message=message)


class LogNotFoundError(AppError):
    def __init__(self, message: str = "日志不存在") -> None:
        from app.core.error_codes import LOG_NOT_FOUND

        super().__init__(status_code=404, code=LOG_NOT_FOUND, message=message)


class ProfileValidationError(AppError):
    def __init__(self, message: str = "个人资料校验失败") -> None:
        from app.core.error_codes import PROFILE_VALIDATION_ERROR

        super().__init__(status_code=400, code=PROFILE_VALIDATION_ERROR, message=message)


class PasswordOldIncorrectError(AppError):
    def __init__(self, message: str = "原密码不正确") -> None:
        from app.core.error_codes import PASSWORD_CHANGE_OLD_INCORRECT

        super().__init__(status_code=400, code=PASSWORD_CHANGE_OLD_INCORRECT, message=message)


class PasswordPolicyError(AppError):
    def __init__(
        self,
        message: str = "新密码不符合安全策略",
        *,
        violations: list[str] | None = None,
        policy: dict[str, Any] | None = None,
    ) -> None:
        from app.core.error_codes import PASSWORD_CHANGE_POLICY

        data: dict[str, Any] | None = None
        if violations is not None:
            data = {"violations": violations}
            if policy is not None:
                data["policy"] = policy
        super().__init__(status_code=400, code=PASSWORD_CHANGE_POLICY, message=message, data=data)


class PasswordWeakError(AppError):
    def __init__(self, message: str = "新密码过于常见，请更换") -> None:
        from app.core.error_codes import PASSWORD_CHANGE_WEAK

        super().__init__(status_code=400, code=PASSWORD_CHANGE_WEAK, message=message)


class PasswordSameAsOldError(AppError):
    def __init__(self, message: str = "新密码不能与原密码相同") -> None:
        from app.core.error_codes import PASSWORD_CHANGE_SAME_AS_OLD

        super().__init__(status_code=400, code=PASSWORD_CHANGE_SAME_AS_OLD, message=message)


class PasswordChangeRateLimitError(AppError):
    def __init__(self, message: str = "改密操作过于频繁，请稍后再试") -> None:
        from app.core.error_codes import PASSWORD_CHANGE_RATE_LIMIT

        super().__init__(status_code=429, code=PASSWORD_CHANGE_RATE_LIMIT, message=message)


class BrandNotFoundError(AppError):
    def __init__(self, message: str = "品牌不存在") -> None:
        super().__init__(status_code=404, code=30010, message=message)


class BrandNameDuplicatedError(AppError):
    def __init__(self, message: str = "品牌名称已存在，请更换") -> None:
        super().__init__(status_code=409, code=30011, message=message)


class BrandDeleteForbiddenError(AppError):
    def __init__(self, message: str = "仅允许删除未关联SKU且已停用的品牌") -> None:
        super().__init__(status_code=409, code=30012, message=message)


class BrandInvalidSortOrderError(AppError):
    def __init__(self, message: str = "品牌排序必须为正整数") -> None:
        super().__init__(status_code=400, code=40020, message=message)


class CategoryNotFoundError(AppError):
    def __init__(self, message: str = "类目不存在") -> None:
        super().__init__(status_code=404, code=30020, message=message)


class CategoryCodeDuplicatedError(AppError):
    def __init__(self, message: str = "类目编码已存在，请更换") -> None:
        super().__init__(status_code=409, code=30021, message=message)


class CategoryDeleteForbiddenError(AppError):
    def __init__(self, message: str = "仅允许删除未绑定SKU且已停用的类目") -> None:
        super().__init__(status_code=409, code=30022, message=message)


class CategoryMaxDepthExceededError(AppError):
    def __init__(self, message: str = "类目最多支持三级，无法继续新增子级") -> None:
        super().__init__(status_code=422, code=30023, message=message)


class CategoryInvalidSortOrderError(AppError):
    def __init__(self, message: str = "排序权重必须为正整数") -> None:
        super().__init__(status_code=400, code=40021, message=message)


class TileSkuNotFoundError(AppError):
    def __init__(self, message: str = "SKU 不存在") -> None:
        super().__init__(status_code=404, code=30030, message=message)


class TileSkuCodeDuplicatedError(AppError):
    def __init__(self, message: str = "SKU 编码已存在，请更换") -> None:
        super().__init__(status_code=409, code=30031, message=message)


class TileSkuDeleteForbiddenError(AppError):
    def __init__(self, message: str = "已上架 SKU 不允许删除") -> None:
        super().__init__(status_code=409, code=30032, message=message)


class TileSkuPublishForbiddenError(AppError):
    def __init__(self, message: str = "SKU 不满足上架条件") -> None:
        super().__init__(status_code=409, code=30033, message=message)


class TileSpecNotFoundError(AppError):
    def __init__(self, message: str = "瓷砖规格不存在") -> None:
        from app.core.error_codes import TILE_SPEC_NOT_FOUND

        super().__init__(status_code=404, code=TILE_SPEC_NOT_FOUND, message=message)


class TileSpecDuplicatedError(AppError):
    def __init__(self, message: str = "该宽长规格已存在，请更换") -> None:
        from app.core.error_codes import TILE_SPEC_DUPLICATED

        super().__init__(status_code=409, code=TILE_SPEC_DUPLICATED, message=message)


class TileSpecDeleteForbiddenError(AppError):
    def __init__(self, message: str = "仅允许删除未关联SKU且已停用的规格") -> None:
        from app.core.error_codes import TILE_SPEC_DELETE_FORBIDDEN

        super().__init__(status_code=409, code=TILE_SPEC_DELETE_FORBIDDEN, message=message)


class TileSpecDisabledError(AppError):
    def __init__(self, message: str = "所选规格已停用，请选择启用规格") -> None:
        from app.core.error_codes import TILE_SPEC_DISABLED

        super().__init__(status_code=400, code=TILE_SPEC_DISABLED, message=message)


class TileSpecInvalidSortOrderError(AppError):
    def __init__(self, message: str = "排序权重必须为正整数") -> None:
        super().__init__(status_code=400, code=40001, message=message)


class BannerNotFoundError(AppError):
    def __init__(self, message: str = "Banner 不存在") -> None:
        from app.core.error_codes import BANNER_NOT_FOUND

        super().__init__(status_code=404, code=BANNER_NOT_FOUND, message=message)


class BannerTitleDuplicatedError(AppError):
    def __init__(self, message: str = "同一展示端与位置下标题已存在") -> None:
        from app.core.error_codes import BANNER_TITLE_DUPLICATED

        super().__init__(status_code=409, code=BANNER_TITLE_DUPLICATED, message=message)


class BannerJumpTargetInvalidError(AppError):
    def __init__(self, message: str = "跳转目标配置无效") -> None:
        from app.core.error_codes import BANNER_JUMP_TARGET_INVALID

        super().__init__(status_code=400, code=BANNER_JUMP_TARGET_INVALID, message=message)


class BannerDeleteForbiddenError(AppError):
    def __init__(self, message: str = "已上线 Banner 不允许删除，请先下线") -> None:
        from app.core.error_codes import BANNER_DELETE_FORBIDDEN

        super().__init__(status_code=409, code=BANNER_DELETE_FORBIDDEN, message=message)


class BannerExternalUrlInvalidError(AppError):
    def __init__(self, message: str = "外部链接必须以 https:// 开头") -> None:
        from app.core.error_codes import BANNER_EXTERNAL_URL_INVALID

        super().__init__(status_code=400, code=BANNER_EXTERNAL_URL_INVALID, message=message)
