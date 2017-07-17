from app.core.exception import ServiceError


class UniqueError(ServiceError):
    code = 600
    message = "重复!"


class FormatError(ServiceError):
    code = 601
    message = "格式错误!"


class LimitError(ServiceError):
    code = 602
    message = "超出访问限制,需要反馈么!"


class CodeError(ServiceError):
    code = 603
    message = "邮件验证码错误!"


class SigninError(ServiceError):
    code = 604
    message = "邮箱或者密码错误!"


class EmailError(ServiceError):
    code = 605
    message = "邮箱已经被注册!"


class NikeNameError(ServiceError):
    code = 606
    message = "此昵称已经被使用!"


class PwdError(ServiceError):
    code = 607
    message = "密码错误!"
