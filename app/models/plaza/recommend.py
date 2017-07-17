import datetime

import pytz
from bson import ObjectId
from mongoengine import Document, IntField, ObjectIdField, NotUniqueError

from app.utils.date_time import DateTimeMixin

BrowseType = {
    "ARTICLE": 1,
    "COMMENT": 2
}


class BrowseRecord(Document):
    """
    浏览记录
    """
    meta = {
        'indexes': [
            {
                'fields': ("rid", "uid"), 'unique': True
            }
        ]
    }
    rid = ObjectIdField(required=True)  # 因为目前只有文章和评论这两个功能，并且均是以ObjectId作为主键，所以这里也是这样
    node = ObjectIdField()
    uid = IntField(required=True)  # who
    count = IntField(default=1)

    @classmethod
    def create_record(cls, rid, node, uid):
        """
        创建浏览记录
        :type rid:objectid
        :type node: objectid
        :type uid:int
        :param rid:
        :param node
        :param uid
        :return: 
        """
        try:
            cls(rid=rid, uid=uid, node=node).save()
        except NotUniqueError:
            ins = cls.objects(rid=rid, uid=uid).first()
            if ins:
                ins.modify(inc__count=1)

    @classmethod
    def search_uid(cls, uid, page, per_page, timestamp=None):
        """
        搜索某人的记录,如果指定时间戳的话，则返回当天的
        :param uid: 
        :param page
        :param per_page
        :param timestamp: 
        :return: 返回node
        """
        query_set = cls.objects(uid=uid)
        if timestamp:
            dt = DateTimeMixin.from_timestamp(timestamp)
            dt_first = datetime.datetime(dt.year, dt.month, dt.day, 0, 0, 1)
            dt_last = datetime.datetime(dt.year, dt.month, dt.day, 23, 23, 59)
            first_bson = ObjectId.from_datetime(dt_first)
            last_bson = ObjectId().from_datetime(dt_last)
            ins = query_set(pk__gte=first_bson, pk__lte=last_bson)
        else:
            ins = query_set
        return ins.order_by("-count").only("node").skip((page - 1) * per_page).limit(per_page)

    def to_dict(self):
        return {
            "time": self.pk.generation_time.timestamp(),
            "rid": str(self.rid),
            "uid": self.uid,
            "node": str(self.node)
        }
