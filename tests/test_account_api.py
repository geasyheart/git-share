from app.models.accounts.exceptions import NikeNameError
from app.models.accounts.users import User, UserCode
from tests.base import MetaTest


class UserApi(MetaTest):
    def ensure_db(self):
        User.drop_collection()
        UserCode.drop_collection()

    def test_send_email_code(self):
        """
        测试发送邮件验证码
        :return:
        """
        uri = "/api/email"
        data = {"email": "110@qq.com"}
        self.app.config.update({"DEBUG": True})
        for i in range(3):
            resp = self.post(uri, data=data)
            self.assertEqual(resp['code'], 0)
        for i in range(10):
            resp = self.post(uri, data=data)
            self.assertEqual(resp['code'], 602)
        data = {"email": "111@qq.com"}
        for i in range(3):
            resp = self.post(uri, data=data)
            self.assertEqual(resp['code'], 0)

    def test_signup(self):
        pass

    def test_signin(self):
        pass

    def test_search_uid(self):
        user = User.signup("110@aa.com", "abcd1234", "lala")
        uid = user.uid
        resp = self.get("/api/user/{}".format(uid))
        self.assertGreater(len(resp.keys()), 1)

    def test_search_nickname(self):
        User.signup("110@aa.com", "abcd1234", "lala")
        resp = self.get('/api/nickname?nickname={}'.format("lala"))
        self.assertEqual(resp["code"], 606)
        resp = self.get('/api/nickname?nickname={}'.format("lala2"))
        self.assertEqual(resp["code"], 0)
