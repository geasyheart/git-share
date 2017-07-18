import random
import string

from flask import current_app, request, session, g, redirect, url_for

from app.core.kit import ServiceView, login_required, geetest_required
from app.core.login import login_user
from app.lib.oauth.github import GitOAuth
from app.models.accounts.exceptions import CodeError, EmailError, FormatError
from app.models.accounts.users import User, UserCode, CODE_PURPOSE
from app.models.oauth.exceptions import UserCancelError, StateError, UserCodeError, UserAccessTokenError, \
    BindTokenError, GitNotBindError
from app.models.oauth.github import GitHubOauth
from app.utils.rtype import verify_email, verify_password
from app.utils.token import Token


class GitAuthApi(ServiceView):
    @staticmethod
    def random_str(length=30):
        return "".join(random.sample(string.ascii_letters + string.digits, length))

    def get(self):
        """
            发送请求
        """
        client_id = current_app.config["GITHUB_CLIENT_ID"]
        redirect_uri = current_app.config["GITHUB_CALLBACK"]
        scope = 'user'
        git = GitOAuth(client_id)
        state = self.random_str()
        session["github_state"] = state
        url = git.authorize(redirect_uri, scope, state)
        return {"url": url}


class GitCallBackApi(ServiceView):
    def get(self):
        """
        回调
        :return: 
        """
        args = request.args
        code = args.get('code')
        state = args.get('state')
        if (not code) or (not state):
            raise UserCancelError
        session_state = session.get('github_state')
        if not session_state:
            raise StateError
        if state != session_state:
            raise StateError
        client_id = current_app.config["GITHUB_CLIENT_ID"]
        client_secret = current_app.config["GITHUB_CLIENT_SECRET"]
        redirect_uri = current_app.config["GITHUB_CALLBACK"]
        git = GitOAuth(client_id, client_secret)
        access_token, scope, token_type = git.access_token(code, redirect_uri)
        if not access_token:
            raise UserCodeError  # 此处还有一个可能，就是授权成功后，仍访问此接口，目前pass
        payload = git.access_api(access_token)
        if not payload:
            raise UserAccessTokenError
        git_nickname = payload["login"]
        cur_uid = g.uid
        if cur_uid > -1:
            # 表示用户已经登录
            git_ins = GitHubOauth.search_uid_nickname(cur_uid, git_nickname)
            if git_ins:
                # 表示用户已经绑定了
                return redirect("/")  # 全部重定向/,此处省事...
            else:
                # 1)用户绑定了，但是不是这个账号
                # 2) 未绑定

                ins = GitHubOauth.search_uid(cur_uid)
                if ins:
                    # 莫非想重新绑定??
                    resp = ins.modify(set__payload=payload, set__nickname=git_nickname)
                    if resp:
                        return redirect("/")
                    else:
                        # 可能昵称重复，目前pass
                        raise BindTokenError
                else:
                    GitHubOauth.create_git(cur_uid, payload, git_nickname)
                    user = User.with_id(cur_uid)
                    html_url = payload["html_url"]
                    user.github = html_url
                    user.save()
                    return redirect("/")

        else:
            git_email = payload.get("email")
            # 表示用户尚未登录/注册,那么通过这个进行绑定
            git_ins = GitHubOauth.search_nickname(git_nickname)
            if git_ins:
                user = User.with_id(git_ins.uid)
                if not user:  # 此时匿名用户
                    session["GIT_ACCESS_TOKEN"] = str(git_ins.pk)
                    user2 = User.search_email(git_email)
                    if user2:
                        return redirect(url_for("index.git_bind", **{"nickname": git_nickname}))
                    return redirect(url_for("index.git_bind", **{"email": git_email, "nickname": git_nickname}))
                redi = redirect("/")
                response = current_app.make_response(redi)
                token = Token(current_app.config['SECRET_KEY'])
                cookie_name = current_app.config["COOKIE_NAME"]
                cookie_max_age = current_app.config["COOKIE_MAX_AGE"]
                response.set_cookie(cookie_name, token.dumps(user.to_encode()), cookie_max_age, httponly=True)
                response.set_cookie('uid', str(user.uid), cookie_max_age)
                return response
            else:
                ins = GitHubOauth.create_git(cur_uid, payload, git_nickname)
                session["GIT_ACCESS_TOKEN"] = str(ins.pk)

                if git_email:
                    user = User.search_email(git_email)
                    if user:
                        return redirect(url_for("index.git_bind", **{"nickname": git_nickname}))
                    return redirect(url_for("index.git_bind", **{"email": git_email, "nickname": git_nickname}))
                return redirect(url_for("index.git_bind", **{"nickname": git_nickname}))


class GitBindApi(ServiceView):
    @login_required
    def get(self):
        """
        检测当前用户是否已经绑定了Github
        :return: 
        """
        uid = g.uid
        git_ins = GitHubOauth.search_uid(uid)
        if not git_ins:
            raise GitNotBindError

    @geetest_required
    def post(self):
        """
        :return: 
        """
        data = request.form
        nickname = data.get('nickname')
        email = data.get('email')
        code = data.get('code')
        pwd = data.get('pwd')
        if not verify_email(email):
            raise FormatError("邮箱格式错误!")
        if not verify_password(pwd):
            raise FormatError("密码格式错误!")
        token = session.get("GIT_ACCESS_TOKEN")
        if not token:
            raise BindTokenError
        git_ins = GitHubOauth.with_id(token)
        if not git_ins:
            raise BindTokenError
        user_code = UserCode.search_code(email, code, CODE_PURPOSE['REGISTER'])
        if not user_code:
            raise CodeError
        user = User.search_email(email)
        if user:
            raise EmailError
        ins = User.signup(email, pwd, nickname)
        payload = git_ins.payload
        html_url = payload.get('html_url')
        # ins.modify(set__github=html_url)
        ins.github = html_url
        ins.save()
        uid = ins.uid
        git_ins.modify(set__uid=uid)
        login_user(uid, ins.to_encode())
        return {
            "payload": ins.to_dict()
        }
