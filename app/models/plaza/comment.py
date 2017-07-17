from mongoengine import Document, ObjectIdField, IntField, StringField


class ArticleComment(Document):
    """
    评论(简洁为主....)
    """
    meta = {
        'indexes': ['rid']
    }
    rid = ObjectIdField(required=True)  # 指向的文章ID
    uid = IntField(required=True)
    floor = IntField()
    content = StringField()  # 内容

    @classmethod
    def with_id(cls, id):
        return cls.objects.with_id(id)

    @classmethod
    def create_comment(cls, rid, uid, floor, content):
        """
        创建评论,
        :type rid: objectid
        :type uid: int
        :type floor: int
        :type content: str
        :param rid: 
        :param uid: 
        :param floor
        :param content: 
        :return: 
        """
        cls(rid=rid, uid=uid, floor=floor, content=content).save()

    @classmethod
    def list_comment(cls, rid, page, per_page):
        """
        
        :param rid: 
        :param page: 
        :param per_page: 
        :return: 
        """
        ins = cls.objects(rid=rid)
        return ins.order_by("-pk").skip((page - 1) * per_page).limit(per_page), ins.count()

    def to_dict(self):
        return {
            "id": str(self.pk),
            "rid": str(self.rid),
            "time": self.pk.generation_time.timestamp(),
            "uid": self.uid,
            "floor": self.floor,
            "content": self.content
        }
