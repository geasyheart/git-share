from mongoengine import Document, IntField, StringField, NotUniqueError
from app.utils.date_time import DateTimeMixin


class FeedbackLimit(Document, DateTimeMixin):
    uid = IntField()
    dt = IntField(unique_with="uid")
    count = IntField()

    @classmethod
    def create_limit(cls, uid):
        today = cls.today()
        ins = cls.objects(uid=uid, dt=today).first()
        if not ins:
            try:
                cls(uid=uid, dt=today, count=1).save()
            except NotUniqueError:
                pass
            else:
                return 1
        else:
            query = {"count__lt": 5}
            return ins.modify(query=query, inc__count=1)


class Feedback(Document):
    uid = IntField()
    content = StringField()

    @classmethod
    def create_feedback(cls, uid, content):
        """
        :type uid: int
        :type content: str
        :param uid: 
        :param content: 
        :return: 
        """
        cls(uid=uid, content=content).save()
