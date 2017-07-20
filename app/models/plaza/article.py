import datetime

from bson import ObjectId
from mongoengine import Document, StringField, ObjectIdField, IntField, BooleanField, NotUniqueError

from app.utils.date_time import DateTimeMixin


class ArticleNode(Document):
    node = StringField(unique=True)  # 父节点
    article_count = IntField()  # 文章数量

    @classmethod
    def with_id(cls, id):
        return cls.objects.with_id(id)

    @classmethod
    def create_node(cls, node_name):
        ins = cls(node=node_name)
        try:
            ins.save()
        except NotUniqueError:
            pass
        return ins

    def to_dict(self):
        return {
            "id": str(self.pk),
            "node": self.node
        }


class Article(Document):
    ORDER_BY = ("pk", "click", "like", "comment", "favorite",
                "-pk", "-click", "-like", "-comment", "-favorite")

    meta = {
        'indexes': ['node']
    }

    title = StringField(required=True)
    body = StringField()
    node = ObjectIdField(required=True)  # 指向ArticleNode主键
    click = IntField(default=0)  # 点击数
    like = IntField(default=0)  # 喜欢数
    comment = IntField(default=0)  # 评论数
    favorite = IntField(default=0)  # 收藏数
    who = IntField()  # 谁
    login = BooleanField()  # 登陆可见
    top = BooleanField(default=False)  # 置顶
    origin = BooleanField(default=True)  # 是否为原创,此处只支持原创和转载两种模式

    @classmethod
    def with_id(cls, id):
        return cls.objects.with_id(id)

    @classmethod
    def create_article(cls, title, body, node, who, login=False, origin=True):
        """
        :type who:int
        :type login: bool
        :param title: 
        :param body: 
        :param node: 
        :param who: 
        :param login: 
        :param origin
        :return: 
        """
        cls(title=title, body=body, node=node, who=who, login=login, origin=origin).save()

    @classmethod
    def list_by_node(cls, node, page, per_page, order_by="-pk"):
        """
        
        :param node: 
        :param page: 
        :param per_page: 
        :param order_by: (time,like,comment,favorite)
        :return: 
        """
        ins = cls.objects(node=node)
        ins_list = ins.order_by("-top", order_by).skip((page - 1) * per_page).limit(per_page)
        count = ins.count()
        return [ins.to_dict() for ins in ins_list], count

    @classmethod
    def list_article(cls, page, per_page, order_by="-pk"):
        """
            
        :param page: 
        :param per_page: 
        :param order_by: 
        :return: 
        """
        ins = cls.objects
        ins_list = ins.order_by("-top", order_by).skip((page - 1) * per_page).limit(per_page)
        count = ins.count()
        return [ins.to_dict() for ins in ins_list], count

    @classmethod
    def search_node(cls, node):
        return cls.objects(node=node).first()

    @classmethod
    def search_week_hot(cls, node, page, per_page):
        now = DateTimeMixin.now()
        week = now - datetime.timedelta(days=7)
        now_bson = ObjectId().from_datetime(now)
        week_bson = ObjectId().from_datetime(week)
        ins = cls.objects(node=node)(pk__gte=week_bson, pk__lte=now_bson).order_by("-click").skip(
            (page - 1) * per_page).limit(per_page)
        return [i.to_dict() for i in ins]

    def to_dict(self, simple=True):
        payload = {
            "id": str(self.pk),
            "node": str(self.node),
            "title": self.title,
            "comment": self.comment,
            "top": self.top,
            "time": self.pk.generation_time.timestamp(),
            "click": self.click,
            "like": self.like,
            "favorite": self.favorite,
            "who": self.who,
            "login": self.login,
            "origin": self.origin
        }
        if not simple:
            payload.update({
                "content": self.body,
            })
        return payload


class Like(Document):
    meta = {
        'indexes': ['rid', 'uid']
    }
    rid = ObjectIdField(required=True)  # 由于目前所有的主键均为objectid,所以这里也直接使用.
    uid = IntField(required=True, unique_with="rid")  # 目前所有简洁为主

    @classmethod
    def search_rid(cls, rid, uid):
        return cls.objects(rid=rid, uid=uid).first()

    @classmethod
    def create_like(cls, rid, uid):
        """
        :type rid: objectid
        :type uid: int
        :param rid: 指向的文章ID 
        :param uid: uid
        :return: 
        """
        try:
            cls(rid=rid, uid=uid).save()
        except NotUniqueError:
            pass

    @classmethod
    def delete_like(cls, rid, uid):
        ins = cls.objects(rid=rid, uid=uid).first()
        if ins:
            ins.delete()
            return True
        return False


class Favorite(Document):
    meta = {
        'indexes': ['rid', 'uid']
    }
    rid = ObjectIdField(required=True)  # 由于目前所有的主键均为objectid,所以这里也直接使用.
    node = ObjectIdField(required=True)  # 表示此文章属于哪一个节点
    title = StringField()
    uid = IntField(required=True, unique_with="rid")  # 目前所有简洁为主

    @classmethod
    def create_favorite(cls, rid, node, title, uid):
        """

            :type rid: objectid
            :type node:objectid
            :type uid: int
            :param rid: 指向的文章ID
            :param node:
            :param title: 表示收藏的文章title,方便展示.
            :param uid: uid
            :return: 
        """
        try:
            cls(rid=rid, node=node, title=title, uid=uid).save()
        except NotUniqueError:
            pass

    @classmethod
    def delete_favorite(cls, rid, uid):
        ins = cls.objects(rid=rid, uid=uid).first()
        if ins:
            ins.delete()
            return True
        return False

    @classmethod
    def search_rid(cls, rid, uid):
        return cls.objects(rid=rid, uid=uid).first()

    def to_dict(self):
        return {
            "time": self.pk.generation_time.timestamp(),
            "rid": str(self.rid),
            "node": str(self.node),
            "title": self.title
        }
