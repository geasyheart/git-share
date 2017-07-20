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
    code = 100
    message = "参数缺失!"


class GeeTestError(ServiceError):
    code = 1000
    message = "验证错误!"


class TokenRequired(ServiceError):
    code = 403
    message = "需要重新授权登录!"


class RoleRequired(ServiceError):
    code = 405
    message = "not allowed!"
