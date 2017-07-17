from flask import current_app

from app.core.kit import add_cookie
from app.utils.token import Token


def login_user(uid, payload):
    """
    登录用户
    :type uid: int
    :type payload : dict
    :param uid
    :param payload:
    :return:
    """
    payload.setdefault("uid", uid)
    token = Token(current_app.config['SECRET_KEY'])
    cookie_name = current_app.config["COOKIE_NAME"]
    cookie_max_age = current_app.config["COOKIE_MAX_AGE"]
    add_cookie(cookie_name, token.dumps(payload), cookie_max_age, httponly=True)
    add_cookie('uid', str(uid), cookie_max_age)

def logout_user(uid):
    pass