import requests
from requests import RequestException


class GitOAuth(object):
    AUTHORIZE_URI = "http://github.com/login/oauth/authorize"
    ACCESS_TOKEN_URI = "https://github.com/login/oauth/access_token"
    USER_URI = "https://api.github.com/user"

    def __init__(self, client_id, client_secret=None):
        """
        :type client_id: str
        :type client_secret: str
        :param client_id: 
        :param client_secret: 
        """
        self.client_id = client_id
        self.client_secret = client_secret

    def authorize(self, redirect_uri, scope, state):
        """
        向Github发送请求
        method: GET
        :type redirect_uri: str
        :type scope: str
        :type state: str
        :param redirect_uri: 
        :param scope: https://developer.github.com/apps/building-integrations/setting-up-and-registering-oauth-apps/about-scopes-for-oauth-apps/
        :param state: 
        :return: 
        """
        return "{}?client_id={}&redirect_uri={}&scope={}&state={}".format(
            self.AUTHORIZE_URI,
            self.client_id,
            redirect_uri,
            scope,
            state
        )

    def access_token(self, code, redirect_uri):
        """
        通过code获取access_token
        method: POST
        :param code: 
        :param redirect_uri
        :return:  access_token,scope,token_type
        """
        url = "{}?client_id={}&client_secret={}&code={}&redirect_uri={}".format(
            self.ACCESS_TOKEN_URI,
            self.client_id,
            self.client_secret,
            code,
            redirect_uri
        )
        payload = self.send_request("POST", url)
        if not payload:
            return (None,) * 3
        access_token = payload.get("access_token")
        scope = payload.get("scope")
        token_type = payload.get("token_type")
        return access_token, scope, token_type

    def access_api(self, access_token):
        """
        method: GET
        :param access_token: 
        :return: 
        """
        uri = "{}?access_token={}".format(self.USER_URI, access_token)
        payload = self.send_request("GET", uri)
        return payload

    def send_request(self, method, url, **kwargs):
        """
        包装requests发送请求
        :param method: 
        :param url: 
        :param kwargs: 
        :return: 
        """
        kwargs.setdefault("headers", {"Accept": "application/json"})
        kwargs.setdefault("timeout", 10)
        try:
            payload = requests.request(method, url, **kwargs).json()
        except RequestException:
            return
        else:
            return payload
