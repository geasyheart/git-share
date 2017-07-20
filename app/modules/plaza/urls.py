from flask import Blueprint

from app.modules.plaza.apis import NodeListApi, ArticleApi, NodeListDetailApi, ArticleListApi, ArticleDetailApi, \
    ArticleLikeApi, ArticleFavoriteApi, ArticleHotApi, ArticleCommentApi, NoticePreApi, NoticeApi, ArticleRecommendApi, \
    FavoriteApi, ArticleUidApi, GitSpiderApi

modules = Blueprint("plaza", __name__, url_prefix="/api")

modules.add_url_rule("/node", view_func=NodeListApi.as_view("node"))
modules.add_url_rule("/article", view_func=ArticleApi.as_view("article"), methods=['POST'])

modules.add_url_rule("/article/node/<node>", view_func=NodeListDetailApi.as_view("node_list"))
modules.add_url_rule('/article', view_func=ArticleListApi.as_view("article_list"))
modules.add_url_rule("/article/<node>/<article>", view_func=ArticleDetailApi.as_view("detail"))

# 点赞
modules.add_url_rule("/like/article/<article_id>", view_func=ArticleLikeApi.as_view("article_like"),
                     methods=['POST', "DELETE"])
modules.add_url_rule("/article/user/<int:uid>", view_func=ArticleUidApi.as_view("article_uid"))
modules.add_url_rule("/favorite/user/<int:uid>", view_func=FavoriteApi.as_view("favorite_get"))

modules.add_url_rule("/favorite/article/<article_id>", view_func=ArticleFavoriteApi.as_view("article_favorite"),
                     methods=['POST', "DELETE"])
# 热议
modules.add_url_rule("/hot/article", view_func=ArticleHotApi.as_view("article_hot"))

# 评论
modules.add_url_rule("/comment/<article_id>", view_func=ArticleCommentApi.as_view("comment"),
                     methods=['GET', 'POST'])
modules.add_url_rule("/comment/<article_id>/<comment_id>", view_func=ArticleCommentApi.as_view("comments"),
                     methods=["DELETE"])
# message
modules.add_url_rule("/message/new", view_func=NoticePreApi.as_view("notice_pre_api"))
modules.add_url_rule("/message", view_func=NoticeApi.as_view("notice"), methods=["GET"])
modules.add_url_rule("/message/<notice_id>", view_func=NoticeApi.as_view("notice_api"), methods=["PUT", "DELETE"])

# 推荐
modules.add_url_rule("/recommend", view_func=ArticleRecommendApi.as_view("recommend"))

# 获取git用户的repo
modules.add_url_rule("/repos", view_func=GitSpiderApi.as_view("git_spider"), methods=['POST'])
