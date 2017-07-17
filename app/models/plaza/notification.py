from mongoengine import Document, IntField, StringField

from app.models.accounts.users import User

NOTICE_STATUS = {
    "UNREAD": 1,
    "READ": 2,
    "DELETE": 3
}


class Notification(Document):
    meta = {
        "indexes": ['to', 'status']
    }
    title = StringField(required=True)
    desc = StringField()
    fm = IntField(db_field="from", required=True)
    to = IntField(required=True)
    url = StringField()  # 链接
    status = IntField(default=NOTICE_STATUS["UNREAD"])

    @classmethod
    def with_id(cls, id):
        return cls.objects.with_id(id)

    @classmethod
    def create_notice(cls, title, fm, to, desc=None, url=None):
        """
        :type fm:int
        :type to: int
        :param title:  
        :param fm: from
        :param to: to
        :param desc: 
        :param url: 
        :return: 
        """
        cls(title=title, desc=desc, fm=fm, to=to, url=url).save()

    @classmethod
    def list_notice(cls, uid, status, page, per_page):
        """
        查出当前用户的通知
        :type uid: int
        :type status: int
        :param uid: 
        :param status:
        :param page
        :param per_page
        :return: 
        """
        if status not in (NOTICE_STATUS["UNREAD"], NOTICE_STATUS["READ"]):
            return []
        return cls.objects(to=uid, status=status).order_by('-pk').skip((page - 1) * per_page).limit(per_page)

    def to_dict(self):
        return {
            "id": str(self.pk),
            "title": self.title,
            "desc": self.desc,
            "from": User.with_id(self.fm).to_dict(),
            "to": self.to,
            "url": self.url,
            "status": self.status,
            "time": self.pk.generation_time.timestamp()
        }
