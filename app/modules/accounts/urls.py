from flask import Blueprint
from app.modules.accounts.apis import GeeTestRequest, MailApi, SignUpApi, SigninApi, UserInfoApi, UserSettings, \
    NicknameApi

modules = Blueprint("accounts", __name__, url_prefix="/api")

modules.add_url_rule("/geetest", view_func=GeeTestRequest.as_view("geetest_r"))
modules.add_url_rule("/email", view_func=MailApi.as_view("email"), methods=['POST'])
modules.add_url_rule("/signup", view_func=SignUpApi.as_view("signup_api"), methods=["POST"])
modules.add_url_rule("/signin", view_func=SigninApi.as_view("signin_api"), methods=["POST"])

# 个人信息
modules.add_url_rule("/user/<int:id>", view_func=UserInfoApi.as_view("userinfo"))
modules.add_url_rule("/settings", view_func=UserSettings.as_view("user_settings"), methods=['POST', 'PUT'])

# 昵称搜索
modules.add_url_rule("/nickname", view_func=NicknameApi.as_view("nickname"))
