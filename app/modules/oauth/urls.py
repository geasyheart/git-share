from flask import Blueprint

from app.modules.oauth.github import GitAuthApi, GitCallBackApi, GitBindApi

modules = Blueprint("oauth", __name__, url_prefix="/api")

modules.add_url_rule("/oauth/github", view_func=GitAuthApi.as_view("authorize"))
modules.add_url_rule("/oauth/github/callback", view_func=GitCallBackApi.as_view("github_callback"))
modules.add_url_rule("/oauth/github/bind", view_func=GitBindApi.as_view("git_bind"), methods=["GET", "POST"])
