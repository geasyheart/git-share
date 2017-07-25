from app.core.exception import ServiceError


class NotFoundError(ServiceError):
    """
    @apiDefine NotFoundError
    @apiError {Integer} 700 没有找到
    """
    code = 700
    message = "没有找到!"


class ArticleError(ServiceError):
    """
    @apiDefine ArticleError
    @apiError {Integer} 701 文章错误
    """
    code = 701
    message = "文章错误!"


class CommentError(ServiceError):
    """
    @apiDefine CommentError
    @apiError {Integer} 702 评论错误
    """
    code = 702
    message = "评论错误!"


class NotificationError(ServiceError):
    """
    @apiDefine NotificationError
    @apiError {Integer} 703 通知错误
    """
    code = 703
    message = "通知错误!"


class FavoriteNotAllowError(ServiceError):
    """
    @apiDefine FavoriteNotAllowError
    @apiError {Integer} 704 主人设置了相关权限,禁止查看
    """
    code = 704
    message = "主人设置了相关权限,禁止查看!"
