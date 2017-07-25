from app.core.exception import ServiceError


class UserCancelError(ServiceError):
    """
    @apiDefine UserCancelError
    @apiError {Integer}  800 用户取消授权
    """
    code = 800
    message = "用户取消授权!"


class StateError(ServiceError):
    """
    @apiDefine StateError
    @apiError {Integer} 801 验证码错误
    """
    code = 801
    message = "验证码错误!"


class UserCodeError(ServiceError):
    """
    @apiDefine UserCodeError
    @apiError {Integer} 802 授权失败
    """
    code = 802
    message = "授权失败!"


class UserAccessTokenError(ServiceError):
    """
    @apiDefine UserAccessTokenError
    @apiError {Integer} 803 获取用户信息失败
    """
    code = 803
    message = "获取用户信息失败!"


class GitNotBindError(ServiceError):
    """
    @apiDefine GitNotBindError 
    @apiError {Integer} 804 Github尚未绑定
    """
    code = 804
    message = "Github尚未绑定!"


class BindTokenError(ServiceError):
    """
    @apiDefine BindTokenError
    @apiError {Integer} 805 绑定失败
    """
    code = 805
    message = "绑定失败!"

