"""Shared API exceptions."""

from __future__ import annotations


class AppError(Exception):
    def __init__(self, *, status_code: int, code: int, message: str) -> None:
        self.status_code = status_code
        self.code = code
        self.message = message
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
