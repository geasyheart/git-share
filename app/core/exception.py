class ServiceError(Exception):
    code = 0
    message = ''

    def __init__(self, message=None):
        if message is not None:
            self.message = message

    def to_dict(self):
        return {
            "code": self.code,
            "message": self.message
        }


class ArgsError(ServiceError):
    """
    @apiDefine ArgsError
    @apiError {Integer} 100 参数错误 
    """
    code = 100
    message = "参数缺失!"


class GeeTestError(ServiceError):
    """
    @apiDefine GeeTestError
    @apiError {Integer} 1000 验证错误
    """
    code = 1000
    message = "验证错误!"


class TokenRequired(ServiceError):
    """
    @apiDefine TokenRequired
    @apiError {Integer} 403 需要重新授权登录
    """
    code = 403
    message = "需要重新授权登录!"


class RoleRequired(ServiceError):
    """
    @apiDefine RoleRequired
    @apiError {Integer} 405 权限不对
    """
    code = 405
    message = "not allowed!"
