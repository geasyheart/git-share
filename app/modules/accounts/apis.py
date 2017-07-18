import json

from flask import current_app, session, request, g
from mongoengine import NotUniqueError

from app.celery_tasks.tasks.email_sender import Email
from app.core.exception import ArgsError
from app.core.kit import ServiceView, GeeTestView, LoginView, add_cookie
from app.core.login import login_user
from app.lib.geetest import GeetestLib
from app.models.accounts.exceptions import FormatError, LimitError, CodeError, SigninError, EmailError, NikeNameError, \
    PwdError
from app.models.accounts.users import UserCode, CODE_PURPOSE, User
from app.utils.passhash import PassHash
from app.utils.rtype import verify_email, verify_nickname
from app.utils.token import Token


class GeeTestRequest(ServiceView):
    def get(self):
        """

        :return:
        """
        geetest_id = current_app.config['GEETEST_ID']
        geetest_key = current_app.config['GEETEST_KEY']
        gt = GeetestLib(geetest_id, geetest_key)
        status = gt.pre_process()
        session[gt.GT_STATUS_SESSION_KEY] = status
        response_str = gt.get_response_str()
        return response_str


class NicknameApi(ServiceView):
    def get(self):
        """
        查询此昵称是否已经使用
        :return: 
        """
        nickname = request.args.get('nickname')
        if nickname and verify_nickname(nickname):
            user = User.objects(_nickname=nickname).only("_nickname").first()
            if user:
                raise NikeNameError


class MailApi(ServiceView):
    def post(self):
        """
        发送邮件

        todo: 实际发送邮件也需要验证一下，但是目前pass，因为还要写前段样式
        如果前端改了，只需要将ServiceView改成GeetestView即可。。
        :return: 
        """
        email = request.form.get('email')
        if not email:
            raise ArgsError(message="邮箱地址须填!")
        if not verify_email(email):
            raise FormatError(message="邮箱格式错误!")
        user = User.search_email(email)
        if user:
            raise EmailError
        code = UserCode.generate_code(email, CODE_PURPOSE['REGISTER'])
        if not code:
            raise LimitError("明天再进行尝试!")
        mode = current_app.config.get("MODE", "CORE")
        if mode == 'DEV':
            return {"email_code": code}
        sender = current_app.config["SENDER"]  # 关于sender,由于只有一个，所以直接写到配置文件中..
        email = Email(sender, email, 1, **{"code": code})
        email.send()


class SignUpApi(GeeTestView):
    def post(self):
        """
        注册
        :return: 
        """
        data = request.form
        email = data.get('email')
        pwd = data.get('pwd')
        code = data.get('code')
        nickname = data.get('nickname')
        ins = UserCode.search_code(email, code, CODE_PURPOSE['REGISTER'])
        if not ins:
            raise CodeError
        ins = User.signup(email, pwd, nickname)
        payload = ins.to_dict()
        login_user(ins.uid, ins.to_encode())
        return {"payload": payload}


class SigninApi(GeeTestView):
    def post(self):
        """
        登录
        :return: 
        """
        data = request.form
        email = data.get('email')
        pwd = data.get('pwd')
        user = User.signin(email, pwd)
        if user:
            payload = user.to_dict()
            login_user(user.uid, user.to_encode())
            return {"payload": payload}
        else:
            raise SigninError


class ForgetPwdApi(GeeTestView):
    def post(self):
        """
        忘记密码
        :return:
        """
        pass


class UserInfoApi(ServiceView):
    def get(self, id):
        """
        返回用户的信息以及其他信息
        :param id: 用户ID
        :return: 
        """
        user_info = User.with_id(id)
        if user_info:
            return user_info.to_dict()


class UserSettings(LoginView):
    def post(self):
        """
        修改个人信息
        :return: 
        """
        data = request.form
        uid = g.uid
        user = User.with_id(uid)
        for key in data:
            if key not in ("nickname", "github", "avatar", "favorite_public"):
                continue
            setattr(user, key, data[key])
        try:
            user.save()
        except NotUniqueError:
            raise ArgsError(message="昵称已经被使用!")
        else:
            return {"payload": user.to_dict()}

    def put(self):
        """
        修改个人密码
        :return: 
        """
        data = request.form
        uid = g.uid
        cur_pwd = data.get('cur_pwd')
        pwd = data.get('pwd')
        user = User.with_id(uid)
        if user:
            b = PassHash.verify(cur_pwd, user.pwd)
            if not b:
                raise PwdError
            user.pwd = pwd
            user.save()
