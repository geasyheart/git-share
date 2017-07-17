from app.core.exception import ServiceError


class NotFoundError(ServiceError):
    code = 700
    message = "没有找到!"


class ArticleError(ServiceError):
    code = 701
    message = "文章错误!"


class CommentError(ServiceError):
    code = 702
    message = "评论错误!"


class NotificationError(ServiceError):
    code = 703
    message = "通知错误!"


class FavoriteNotAllowError(ServiceError):
    code = 704
    message = "主人设置了相关权限,禁止查看!"
