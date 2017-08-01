import random
import string

from mongoengine import Document, IntField, StringField, SequenceField, NotUniqueError, BooleanField

from app.core.exception import ArgsError
from app.models.accounts.exceptions import UniqueError
from app.utils.date_time import DateTimeMixin
from app.utils.passhash import PassHash
from app.utils.rtype import verify_nickname, verify_password, verify_url


class User(Document):
    uid = SequenceField(primary_key=True, required=True)  # type:int
    _nickname = StringField(db_field="nickname", required=True, unique=True)
    email = StringField(required=True, unique=True)
    _pwd = StringField(db_field="pwd", required=True)
    role = IntField(default=1)
    gender = IntField(db_field="gender")
    _github = StringField(db_field="github")
    avatar = StringField(default='/static/public/avatar/0.png')  # 这里就先放在这..
    fp = BooleanField(db_field="fp", default=True)  # 收藏是否公开

    @property
    def nickname(self):
        return self._nickname

    @nickname.setter
    def nickname(self, value):
        if not verify_nickname(value):
            raise ArgsError(message="请使用英文字母或数字,最少3位!!")
        self._nickname = value

    @property
    def pwd(self):
        return self._pwd

    @pwd.setter
    def pwd(self, value):
        if not verify_password(value):
            raise ArgsError(message="密码格式不对!")
        self._pwd = PassHash.encrypt(value)

    @property
    def github(self):
        return self._github

    @github.setter
    def github(self, value):
        if value:
            if not verify_url(value):
                raise ArgsError(message="URL格式不对!")
        self._github = value

    @property
    def favorite_public(self):
        return self.fp

    @favorite_public.setter
    def favorite_public(self, value):
        try:
            value = int(value)
        except ValueError:
            pass
        else:
            self.fp = bool(value)

    @classmethod
    def with_id(cls, uid):
        return cls.objects.with_id(uid)

    @classmethod
    def search_email(cls, email):
        """

        :param email:
        :return:
        """
        return cls.objects(email=email).first()

    @classmethod
    def search_nickname(cls, nickname):
        return cls.objects(_nickname=nickname).first()

    @classmethod
    def signup(cls, email, pwd, nickname):
        """

        :param email:
        :param pwd:
        :param nickname:
        :return:
        """
        ins = cls(email=email)
        ins.nickname = nickname
        ins.pwd = pwd
        try:
            ins.save(force_insert=True)
        except NotUniqueError:
            eins = cls.search_email(email)
            if eins:
                raise UniqueError(message="邮箱已经被注册!")
            nins = cls.search_nickname(nickname)
            if nins:
                raise UniqueError(message="昵称已经被使用!")
        else:
            return ins

    @classmethod
    def signin(cls, email, pwd):
        """

        :param email:
        :param pwd:
        :return:
        """
        ins = cls.objects(email=email).first()
        if ins:
            b = PassHash.verify(pwd, ins.pwd)
            if b:
                return ins

    def to_dict(self, simple=True):
        payload = {
            "uid": self.uid,
            "nickname": self.nickname,
            "role": self.role,
            "gender": self.gender,
            "avatar": self.avatar,
            "github": self.github,
            "fp": self.favorite_public
        }
        if not simple:
            payload.update({
                "email": self.email
            })
        return payload

    def to_encode(self):
        return {
            "uid": self.uid,
            "role": self.role
        }


CODE_PURPOSE = {
    "REGISTER": 1,
    "FORGET": 2
}


class UserCode(Document, DateTimeMixin):
    meta = {
        'indexes': ['email', 'dt', 'tp']
    }
    email = StringField(required=True)
    dt = IntField()
    code = StringField()
    count = IntField(max_value=3)
    tp = IntField(default=CODE_PURPOSE["REGISTER"])

    @classmethod
    def search_code(cls, email, code, tp):
        """

        :param email:
        :param code:
        :param tp
        :return:
        """
        _today = cls.today()
        return cls.objects(email=email, dt=_today, code=code, tp=tp).first()

    @classmethod
    def generate_code(cls, email, tp):
        """
        生成邮件验证码
        :param email:
        :param tp:
        :return: 
        """
        _today = cls.today()
        code = "".join(random.sample(string.ascii_letters + string.digits, 6))
        ins = cls.objects(email=email, dt=_today, tp=tp).first()
        if ins:
            query = {"count__lt": 3}
            b = ins.modify(query=query, inc__count=1, set__code=code)
            if b:
                return code
        else:
            cls(email=email, dt=_today, code=code, count=1, tp=tp).save()
            return code


class EmailTemplate(Document):
    id = SequenceField(required=True, primary_key=True)
    subject = StringField(required=True)
    temp = StringField()  # 模板
    remark = StringField()

    @classmethod
    def create_temp(cls, subject, temp, id=None, remark=None):
        if id:
            cls(id=id, subject=subject, temp=temp, remark=remark).save()
        else:
            cls(subject=subject, temp=temp, remark=remark).save()

    @classmethod
    def with_id(cls, temp_id):
        return cls.objects.with_id(temp_id)
