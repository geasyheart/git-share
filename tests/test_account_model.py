from app.core.exception import ArgsError
from app.models.accounts.exceptions import UniqueError
from app.models.accounts.users import User, UserCode, CODE_PURPOSE
from tests.base import MetaTest


class AccountTest(MetaTest):
    def ensure_db(self):
        User.drop_collection()
        UserCode.drop_collection()

    def test_code(self):
        """
        测试生成验证码
        :return:
        """
        count = 0
        emails = ('11{}@qq.com'.format(i) for i in range(100))
        for email in emails:
            for i in range(10):
                code = UserCode.generate_code(email, CODE_PURPOSE['REGISTER'])
                if code:
                    count += 1
        self.assertEqual(count, 300)

    def test_signup(self):
        """
        测试注册
        :return:
        """
        emails = ('11{}@qq.com'.format(i) for i in range(100))
        [User.signup(email, "abcd1234", "nickname{}".format(i)) for i, email in enumerate(emails)]
        self.assertEqual(User.objects.count(), 100)
        with self.assertRaises(ArgsError):
            User.signup("1@qq.com", "abcd1234", '昵称')

        with self.assertRaises(ArgsError):
            User.signup('1@qq.com', 'a1', "abcda")

        with self.assertRaises(UniqueError):
            User.signup("110@qq.com", 'abcd1234', 'aaaaa')

        with self.assertRaises(UniqueError):
            User.signup('a@aa.com', 'abdc1234', 'nickname1')

    def test_signin(self):
        """
        测试登录
        :return: 
        """
        User.signup("110@aa.com", 'abcd1234', 'abbbb')
        resp = User.signin("110@aa.com", 'aaa')
        self.assertIsNone(resp)
        resp = User.signin("1120@aa.com", 'abcd1234')
        self.assertIsNone(resp)
        resp = User.signin("110@aa.com", 'abcd1234')
        self.assertIsNotNone(resp)



