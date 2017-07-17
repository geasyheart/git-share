from functools import wraps

from flask import g, make_response, current_app, request, session
from flask import jsonify
from flask.views import MethodView

from app.core.exception import ServiceError, GeeTestError, ArgsError, TokenRequired
from app.lib.geetest import GeetestLib
from app.utils.token import Token


def add_cookie(key, value, max_age=None, expires=None, path='/', domain=None, secure=None, httponly=False):
    """
    max_age: utc时间，例如保存1天，那么: 8*3600 + 86400
    add_cookie("token", "a123.asd.432", 115000, httponly=True)
    """
    if not hasattr(g, 'cookie_store'):
        g.cookie_store = dict()
    g.cookie_store[key] = (value, max_age, expires, path, domain, secure, httponly)


def service_response(**kwargs):
    """
    只接受json格式数据
    :param kwargs:
    :return:
    """
    kwargs.setdefault("code", 0)  # 微服务提供的错误
    rv = jsonify(**kwargs)
    if hasattr(g, "cookie_store"):
        for k in g.cookie_store:
            # 要将其转成bytes
            rv.set_cookie(k.encode(), *[i.encode() if isinstance(i, str) else i for i in g.cookie_store[k]])
    return rv


def api_view(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            resp = func(*args, **kwargs)
        except ServiceError as e:
            return service_response(**e.to_dict())
        else:
            if not resp:
                return service_response()
            if isinstance(resp, dict):
                return service_response(**resp)
            else:
                # 改动这个地方，因为非jsonify返回，add_cookie不会工作，另外这个地方仍需要测试,因为不确定Python3是否需要encode,之前不写encode也可以.
                response = make_response(resp)
                if hasattr(g, 'cookie_store'):
                    for k in g.cookie_store:
                        response.set_cookie(k.encode(),
                                            *[i.encode() if isinstance(i, str) else i for i in g.cookie_store[k]])
                return response

    return wrapper


def current_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        g.uid, g.role = -1, -1
        cookie_name = current_app.config["COOKIE_NAME"]
        cookie = request.cookies.get(cookie_name)
        if cookie:
            token_obj = Token(current_app.config['SECRET_KEY'])
            rs = token_obj.loads(cookie)
            if rs:
                g.uid = rs.get("uid")
                g.role = rs.get("role")
        return func(*args, **kwargs)

    return wrapper


class ServiceView(MethodView):
    decorators = [api_view, current_user]

    # def get_json(self, schema, *args, **kwargs):
    #     """
    #     关于这个地方，嗯,,,,觉得直接提供的挺好
    #     json进行接收数据
    #     :param schema:
    #     :return:
    #     """
    #     data = request.get_json(*args, **kwargs)
    #     if data is None:
    #         return {}
    #     if isinstance(schema, Schema):
    #         data, errors = schema.load(data)
    #         if errors:
    #             raise ArgsError(errors)
    #         return data


def geetest_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        geetest_id = current_app.config['GEETEST_ID']
        geetest_key = current_app.config['GEETEST_KEY']
        gt = GeetestLib(geetest_id, geetest_key)
        challenge = request.form.get(gt.FN_CHALLENGE)
        validate = request.form.get(gt.FN_VALIDATE)
        seccode = request.form.get(gt.FN_SECCODE)
        if (not challenge) or (not validate) or (not seccode):
            return service_response(**ArgsError().to_dict())
        status = session[gt.GT_STATUS_SESSION_KEY]
        if status:
            result = gt.success_validate(challenge, validate, seccode, None)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        if not result:
            return service_response(**GeeTestError().to_dict())
        return func(*args, **kwargs)

    return wrapper


class GeeTestView(MethodView):
    decorators = [api_view, geetest_required]


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        cookie_name = current_app.config["COOKIE_NAME"]
        cookie = request.cookies.get(cookie_name)
        if not cookie:
            return service_response(**TokenRequired().to_dict())
        token_obj = Token(current_app.config['SECRET_KEY'])
        rs = token_obj.loads(cookie)
        if not rs:
            return service_response(**TokenRequired().to_dict())
        g.uid = rs.get("uid")
        g.role = rs.get("role")
        return func(*args, **kwargs)

    return wrapper


class LoginView(MethodView):
    decorators = [api_view, login_required]
