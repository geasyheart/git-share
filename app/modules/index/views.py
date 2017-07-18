from flask import render_template
from flask.views import MethodView


class IndexHandler(MethodView):
    def get(self):
        return render_template("index.html")


class EditorHandler(MethodView):
    def get(self):
        return render_template("git-pub.html")


class SignupHandler(MethodView):
    def get(self):
        return render_template("signup.html")


class SigninHandler(MethodView):
    def get(self):
        return render_template("signin.html")


class ArticleDetailHandler(MethodView):
    def get(self, node, article):
        """
        这里我一直再考虑要不要做成模板的形式，但是觉得没必要..
        :param node: 
        :param article: 
        :return: 
        """

        return render_template("article_detail.html")


class MessageHandler(MethodView):
    def get(self):
        return render_template("message.html")


class UserHandler(MethodView):
    def get(self, uid):
        return render_template("user.html")


class UserSettingHandler(MethodView):
    def get(self):
        return render_template("settings.html")


class GitHubBindHandler(MethodView):
    def get(self):
        return render_template("git-bind.html")

