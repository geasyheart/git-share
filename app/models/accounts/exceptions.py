from app.core.exception import ServiceError


class UniqueError(ServiceError):
    """
    @apiDefine UniqueError
    @apiError {Integer} 600 重复
    """
    code = 600
    message = "重复!"


class FormatError(ServiceError):
    """
    @apiDefine FormatError
    @apiError  {Integer} 601 格式错误 
    """
    code = 601
    message = "格式错误!"


class LimitError(ServiceError):
    """
    @apiDefine LimitError
    @apiError {Integer} 602 访问限制
    """
    code = 602
    message = "超出访问限制,需要反馈么!"


class CodeError(ServiceError):
    """
    @apiDefine CodeError
    @apiError {Integer} 603 邮箱验证码错误
    """
    code = 603
    message = "邮件验证码错误!"


class SigninError(ServiceError):
    """
    @apiDefine SigninError
    @apiError {Integer} 604 邮箱或者密码错误
    """
    code = 604
    message = "邮箱或者密码错误!"


class EmailError(ServiceError):
    """
    @apiDefine EmailError
    @apiError {Integer} 605 邮箱已经被注册
    """
    code = 605
    message = "邮箱已经被注册!"


class NikeNameError(ServiceError):
    """
    @apiDefine NickNameError
    @apiError {Integer} 606 昵称已经被使用
    """
    code = 606
    message = "此昵称已经被使用!"


class PwdError(ServiceError):
    """
    @apiDefine PwdError
    @apiError {Integer} 607 密码错误
    """
    code = 607
    message = "密码错误!"
