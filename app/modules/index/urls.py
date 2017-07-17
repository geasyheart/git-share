from flask import Blueprint

from app.modules.index.views import IndexHandler, EditorHandler, SignupHandler, SigninHandler, ArticleDetailHandler, \
    MessageHandler, UserHandler, UserSettingHandler, GitHubBindHandler, GitHubBindSuccessHandler

modules = Blueprint("index", __name__)

modules.add_url_rule("/", view_func=IndexHandler.as_view("index"))
modules.add_url_rule("/git-pub", view_func=EditorHandler.as_view("editor"))
modules.add_url_rule("/signup", view_func=SignupHandler.as_view("signup"))
modules.add_url_rule("/signin", view_func=SigninHandler.as_view("signin"))
modules.add_url_rule("/article/<node>/<article>", view_func=ArticleDetailHandler.as_view("article_detail"))
modules.add_url_rule("/message", view_func=MessageHandler.as_view("message"))
modules.add_url_rule("/user/<uid>", view_func=UserHandler.as_view("user_page"))
modules.add_url_rule("/settings", view_func=UserSettingHandler.as_view("settings"))
modules.add_url_rule("/git-bind",view_func=GitHubBindHandler.as_view("git_bind"))
modules.add_url_rule("/git-bind-success",view_func=GitHubBindSuccessHandler.as_view("git_bind_success"))