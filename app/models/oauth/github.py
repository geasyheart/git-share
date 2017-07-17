from mongoengine import Document, DictField, IntField, StringField, NotUniqueError


class GitHubOauth(Document):
    meta = {
        'collection': 'github_oauth'
    }
    uid = IntField(default=-1)  # 这个指向User的uid
    payload = DictField()  # 这里保存用户授权后的信息，由于目前不确定，所以直接保存起来
    nickname = StringField(unique=True)  # 以用户的nickname区分用户

    @classmethod
    def with_id(cls, id):
        return cls.objects.with_id(id)

    @classmethod
    def search_uid_nickname(cls, uid, nickname):
        return cls.objects(uid=uid, nickname=nickname).first()

    @classmethod
    def search_uid(cls, uid):
        return cls.objects(uid=uid).first()

    @classmethod
    def search_nickname(cls,nickname):
        return cls.objects(nickname=nickname).first()

    @classmethod
    def create_git(cls, uid, payload, nickname):
        ins = cls(uid=uid, payload=payload, nickname=nickname)
        try:
            ins.save()
        except NotUniqueError:
            return cls.objects(nickname=nickname).first()
        else:
            return ins
