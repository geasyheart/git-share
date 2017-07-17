from app.core.exception import ServiceError


class UserCancelError(ServiceError):
    code = 800
    message = "用户取消授权!"


class StateError(ServiceError):
    code = 801
    message = "验证码错误!"


class UserCodeError(ServiceError):
    code = 802
    message = "授权失败!"


class UserAccessTokenError(ServiceError):
    code = 803
    message = "获取用户信息失败!"


class GitNotBindError(ServiceError):
    code = 804
    message = "Github尚未绑定!"


class BindTokenError(ServiceError):
    code = 805
    message = "绑定失败!"

