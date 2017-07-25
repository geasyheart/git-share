import datetime
import operator

from bson import ObjectId
from flask import request, g

import time

from app.celery_tasks.tasks.git_info import get_user_git
from app.core.exception import ArgsError
from app.core.kit import ServiceView, LoginView, login_required, require_priv
from app.models.accounts.users import User
from app.models.plaza.article import ArticleNode, Article, Like, Favorite
from app.models.plaza.comment import ArticleComment
from app.models.plaza.exceptions import NotFoundError, ArticleError, CommentError, NotificationError, \
    FavoriteNotAllowError
from app.models.plaza.notification import Notification, NOTICE_STATUS
from app.models.plaza.recommend import BrowseRecord
from app.utils.date_time import DateTimeMixin


def parse_objectid(objectid):
    """
    校验objectid是否为真
    :param objectid: 
    :return: 
    """
    try:
        ObjectId(objectid)
    except:
        raise ArgsError("此参数不对!")


class NodeListApi(ServiceView):
    def get(self):
        """
        @apiVersion 1.0.0
        @api {get} /api/node 返回所有的节点 
        @apiName NodeListApi
        @apiGroup plaza
        
        @apiSuccess {Integer} code 0
        @apiSuccessExample {json} Success-Response:
        {
            "code": 0,
            "node":[
                {
                    "id": "asdfafasdfafadfadfa",
                    "node": "adsfafsajfajf"
                },
                {
                    "id": "asdfafasdfafadfadfa2",
                    "node": "adsfafsajfajf"
                },
            ]
        }
        """
        rs = ArticleNode.objects.all()
        result = {}
        if rs:
            result["node"] = [i.to_dict() for i in rs]
        return result


class ArticleApi(LoginView):
    def post(self):
        """
        @apiVersion 1.0.0
        @api {post} /api/article 发布文章 
        @apiName ArticleApi
        @apiGroup plaza
        
        @apiParam {String} title 题目
        @apiParam {String} content 正文
        @apiParam {String} node 节点
        @apiParam {Boolean} login 登录
        
        
        @apiUse ArgsError
        @apiUse NotFoundError
        @apiUse TokenRequired
        """
        form = request.form
        title = form.get('title')
        content = form.get('content')
        node = form.get('node')
        login = bool(form.get('login', default=False, type=int))
        if (not title) or (not node):
            raise ArgsError("参数不准为空!")
        parse_objectid(node)
        if len(title) > 100:
            raise ArgsError("题目最长100,内容最长10000!")
        if content and len(content) > 10000:
            raise ArgsError("题目最长100,内容最长10000!")
        an_ins = ArticleNode.with_id(node)
        if not an_ins:
            raise NotFoundError("此节点未找到!")
        an_ins.modify(inc__article_count=1)
        Article.create_article(title, content, node, g.uid, login)

    def put(self):
        """
        修改
        :return: 
        """
        pass


class NodeListDetailApi(ServiceView):
    def get(self, node):
        """
        @apiVersion 1.0.0
        @api {get} /api/article/node/:node 根据节点返回文章列表 
        @apiName NodeListDetailApi
        @apiGroup plaza
        
        @apiParam {String} node ObjectId类型
        @apiParam {String} page 第几页
        @apiParam {String} per_page 每页多少
        @apiParam {String} order_by 排序规则
        
        @apiSuccess {Integer} code 0
        @apiSuccessExample {json} Success-Response:
        {
            "code": 0,
            "articles": [
                {
                    "id": "asdfa",
                    "node": "asd",
                    "title": "a",
                    "comment": "a",
                    "top": true,
                    "time": 1233213213,
                    "click": 123,
                    "like": 32,
                    "favorite": true,
                    "who": 123,
                    "login": true,
                    "origin": true"
                },
                {
                    "id": "asdfa",
                    "node": "asd",
                    "title": "a",
                    "comment": "a",
                    "top": true,
                    "time": 1233213213,
                    "click": 123,
                    "like": 32,
                    "favorite": true,
                    "who": 123,
                    "login": true,
                    "origin": true"
                }
                ...
            ],
            "users": [
                {
                    "uid": 123,
                    "nickname": "asdf",
                    "role": 1,
                    "gender": 1,
                    "avatar": "www.ggadsf.com/asdfsafd.img",
                    "github": "github.com/adsfasdf",
                    "fp": true
                },
                {
                    "uid": 123,
                    "nickname": "asdf",
                    "role": 1,
                    "gender": 1,
                    "avatar": "www.ggadsf.com/asdfsafd.img",
                    "github": "github.com/adsfasdf",
                    "fp": true
                }
            ],
            "count": 123
            
        }
        """
        parse_objectid(node)
        args = request.args
        page = args.get('page', default=1, type=int)
        per_page = args.get('per_page', default=10, type=int)
        order_by = args.get('order_by', default='-pk')
        if page < 1: page = 1
        if per_page >= 20: per_page = 20
        if order_by not in Article.ORDER_BY:
            order_by = "-pk"
        articles, count = Article.list_by_node(node, page, per_page, order_by)
        uids = {i["who"] for i in articles}
        users = [User.with_id(uid).to_dict() for uid in uids]
        return {"articles": articles, "users": users, 'count': count}


class ArticleListApi(ServiceView):
    def get(self):
        """
        @apiVersion 1.0.0
        @api {get} /api/article 返回文章列表
        @apiName ArticleListApi
        @apiGroup plaza
        
        @apiParam {String} page 第几页
        @apiParam {String} per_page 每页多少
        @apiParam {String} order_by 排序规则
        
        @apiSuccess {Integer} code 0
        @apiSuccessExample {json} Success-Response:
        {
            "code": 0,
            "articles": [
                {
                    "id": "asdfa",
                    "node": "asd",
                    "title": "a",
                    "comment": "a",
                    "top": true,
                    "time": 1233213213,
                    "click": 123,
                    "like": 32,
                    "favorite": true,
                    "who": 123,
                    "login": true,
                    "origin": true"
                },
                {
                    "id": "asdfa",
                    "node": "asd",
                    "title": "a",
                    "comment": "a",
                    "top": true,
                    "time": 1233213213,
                    "click": 123,
                    "like": 32,
                    "favorite": true,
                    "who": 123,
                    "login": true,
                    "origin": true"
                }
                ...
            ],
            "users": [
                {
                    "uid": 123,
                    "nickname": "asdf",
                    "role": 1,
                    "gender": 1,
                    "avatar": "www.ggadsf.com/asdfsafd.img",
                    "github": "github.com/adsfasdf",
                    "fp": true
                },
                {
                    "uid": 123,
                    "nickname": "asdf",
                    "role": 1,
                    "gender": 1,
                    "avatar": "www.ggadsf.com/asdfsafd.img",
                    "github": "github.com/adsfasdf",
                    "fp": true
                }
            ],
            "count": 123
            
        }
         
        """
        args = request.args
        page = args.get('page', default=1, type=int)
        per_page = args.get('per_page', default=10, type=int)
        order_by = args.get('order_by', default='-pk')
        if page < 1: page = 1
        if per_page >= 20: per_page = 20
        if order_by not in Article.ORDER_BY:
            order_by = "-pk"
        articles, count = Article.list_article(page, per_page, order_by)
        uids = {i["who"] for i in articles}
        users = [User.with_id(uid).to_dict() for uid in uids]
        return {"articles": articles, "users": users, "count": count}


class ArticleDetailApi(ServiceView):
    def get(self, node, article):
        """
        @apiVersion 1.0.0
        @api {get} /api/article/:node/:article 返回文章
        @apiName ArticleDetailApi
        @apiGroup plaza
        
        @apiParam {String} node 节点
        @apiParam {String} article 文章id
        
        @apiSuccess {Integer} code 0
        @apiSuccessExample {json} Success-Response:
        {
            "code": 0,
            "id": "asdfa",
            "node": "asd",
            "title": "a",
            "comment": "a",
            "top": true,
            "time": 1233213213,
            "click": 123,
            "like": 32,
            "favorite": true,
            "who": 123,
            "login": true,
            "origin": true,
            "content":"hello world!",
            "like_bool": true,
            "favorite_bool": true
        }
        @apiUse ArgsError
        @apiUse ArticleError
        """
        parse_objectid(article)
        uid = g.uid
        ins = Article.with_id(article)
        if not ins:
            raise ArticleError("没有找到此文章!")
        ins.modify(inc__click=1)
        payload = ins.to_dict(simple=False)  # 文章详情
        who = ins.who
        user = User.with_id(who)
        payload.update(user.to_dict())
        like = Like.search_rid(article, uid)
        if like:
            payload.update({"like_bool": True})
        else:
            payload.update({"like_bool": False})
        favorite = Favorite.search_rid(article, uid)
        if favorite:
            payload.update({"favorite_bool": True})
        else:
            payload.update({"favorite_bool": False})
        #
        if uid > -1:
            BrowseRecord.create_record(article, ins.node, uid)
        return payload


class ArticleHotApi(ServiceView):
    def get(self):
        """
        @apiVersion 1.0.0
        @api {get} /api/hot/article 返回最近一月热议的项目
        @apiName ArticleHotApi
        @apiGroup plaza
        
        @apiSuccess {Integer} code 0
        @apiSuccessExample {json} Success-Response:
        {
            "code": 0,
            "articles": [
                {
                    "id": "asdfa",
                    "node": "asd",
                    "title": "a",
                    "comment": "a",
                    "top": true,
                    "time": 1233213213,
                    "click": 123,
                    "like": 32,
                    "favorite": true,
                    "who": 123,
                    "login": true,
                    "origin": true"
                },
                {
                    "id": "asdfa",
                    "node": "asd",
                    "title": "a",
                    "comment": "a",
                    "top": true,
                    "time": 1233213213,
                    "click": 123,
                    "like": 32,
                    "favorite": true,
                    "who": 123,
                    "login": true,
                    "origin": true"
                }
                ...
            ],
            "users": [
                {
                    "uid": 123,
                    "nickname": "asdf",
                    "role": 1,
                    "gender": 1,
                    "avatar": "www.ggadsf.com/asdfsafd.img",
                    "github": "github.com/adsfasdf",
                    "fp": true
                },
                {
                    "uid": 123,
                    "nickname": "asdf",
                    "role": 1,
                    "gender": 1,
                    "avatar": "www.ggadsf.com/asdfsafd.img",
                    "github": "github.com/adsfasdf",
                    "fp": true
                }
            ],
            "count": 123
            
        }
        
        """
        today_first = DateTimeMixin.now()
        today_bson = ObjectId().from_datetime(today_first)
        month_first = today_first - datetime.timedelta(days=30)
        month_bson = ObjectId().from_datetime(month_first)
        articles = Article.objects(pk__gte=month_bson, pk__lte=today_bson).order_by('-comment').limit(10)
        uids = {i.who for i in articles}
        users = [User.with_id(uid).to_dict() for uid in uids]
        return {"articles": [article.to_dict() for article in articles], "users": users}


class ArticleUidApi(ServiceView):
    def get(self, uid):
        """
        @apiVersion 1.0.0
        @api {get} /api/user/:uid 根据uid返回创建的文章
        @apiName ArticleUidApi
        @apiGroup plaza
        
        @apiParam {Integer} uid 用户ID
        @apiParam {Integer} page 第几页
        @apiParam {Integer} per_page 每页多少
        
        @apiSuccess {Integer} code 0
        @apiSuccessExample {json} Success-Response:
        {
            "code": 0,
            "articles": [
                {
                    "node": "123",
                    "id": "12321",
                    "title": "asdfafd",
                    "time": 123231234,
                },
                {
                    "node": "123",
                    "id": "12321",
                    "title": "asdfafd",
                    "time": 123231234,
                },
                ...
            ],
            "count": 1234
        }
        """
        page = request.args.get('page', type=int, default=1)
        per_page = request.args.get('per_page', type=int, default=10)
        if page < 1: page = 1
        if per_page >= 20: per_page = 20
        article_ins = Article.objects(who=uid)
        articles = article_ins.skip((page - 1) * per_page).limit(per_page)
        count = article_ins.count()
        return {"articles": [
            {"node": str(i.node), "id": str(i.pk), "title": i.title, "time": i.pk.generation_time.timestamp()} for i in
            articles], "count": count}


class ArticleLikeApi(LoginView):
    def post(self, article_id):
        """
        @apiVersion 1.0.0
        @api {post} /api/like/article/:article_id 点赞
        @apiName ArticleLikeApi
        @apiGroup plaza 
        
        @apiSuccess {Integer} code 0
        
        @apiUse ArgsError
        @apiUse ArticleError
        @apiUse TokenRequired
        """
        parse_objectid(article_id)
        uid = g.uid
        article = Article.with_id(article_id)
        if not article:
            raise ArticleError("文章没有找到!")
        article.modify(inc__like=1)
        Like.create_like(article_id, uid)

    def delete(self, article_id):
        """
        @apiVersion 1.0.0
        @api {delete} /api/like/article/:article_id 取消点赞
        @apiName ArticleLikeApi2
        @apiGroup plaza 
        
        @apiSuccess {Integer} code 0
        
        @apiUse ArgsError
        @apiUse ArticleError
        @apiUse TokenRequired
        """
        parse_objectid(article_id)
        uid = g.uid
        article = Article.with_id(article_id)
        if not article:
            raise ArticleError("文章没有找到!")
        resp = Like.delete_like(article_id, uid)
        if resp:
            article.modify(query={"like__gt": 0}, dec__like=1)


class FavoriteApi(ServiceView):
    def get(self, uid):
        """
        
        @apiVersion 1.0.0
        @api {get} /api/favorite/user/:uid 返回某人的收藏
        @apiName FavoriteApi
        @apiGroup plaza  
        
        @apiParam {Integer} uid 用户ID
        @apiParam {Integer} page 第几页
        @apiParam {Integer} per_page 每页多少
        
        @apiSuccess {Integer} code 0
        @apiSuccessExample {json} Success-Response:
        {
            "favorite": [
                {
                    "time": 123,
                    "rid": "123",
                    "node": "123",
                    "title": "title"
                },
                {
                    "time": 123,
                    "rid": "123",
                    "node": "123",
                    "title": "title"
                }
                
            ],
            "count": 123
        }
        
        @apiUse FavoriteNotAllowError
        """
        page = request.args.get('page', type=int, default=1)
        per_page = request.args.get('per_page', type=int, default=10)
        if page < 1: page = 1
        if per_page > 20: per_page = 20
        cur_uid = g.uid
        user = User.objects(uid=uid).only("fp").first()
        if user:
            fp = user.fp
            if fp:
                ins = Favorite.objects(uid=uid)
                favorite = ins.order_by("-pk").skip((page - 1) * per_page).limit(per_page)
                count = ins.count()
                return {"favorite": [i.to_dict() for i in favorite], "count": count}
            else:
                if cur_uid == uid:
                    ins = Favorite.objects(uid=uid)
                    favorite = ins.order_by("-pk").skip((page - 1) * per_page).limit(per_page)
                    count = ins.count()
                    return {"favorite": [i.to_dict() for i in favorite], "count": count}
                else:
                    raise FavoriteNotAllowError


class ArticleFavoriteApi(LoginView):
    def post(self, article_id):
        """
        
        @apiVersion 1.0.0
        @api {post} /api/favorite/article/:article_id 收藏文章 
        @apiName ArticleFavoriteApi
        @apiGroup plaza  
        
        @apiSuccess {Integer} code 0 
        
        @apiUse ArgsError
        @apiUse ArticleError
        
        """
        parse_objectid(article_id)
        uid = g.uid
        article = Article.with_id(article_id)
        if not article:
            raise ArticleError("文章没有找到!")
        article.modify(inc__favorite=1)

        Favorite.create_favorite(article_id, article.node, article.title, uid)

    def delete(self, article_id):
        """
        
        @apiVersion 1.0.0
        @api {delete} /api/favorite/article/:article_id 取消收藏文章 
        @apiName ArticleFavoriteApi2
        @apiGroup plaza  
        
        @apiSuccess {Integer} code 0 
        
        @apiUse ArgsError
        @apiUse ArticleError
        
        """
        parse_objectid(article_id)
        uid = g.uid
        article = Article.with_id(article_id)
        if not article:
            raise ArticleError("文章没有找到!")
        resp = Favorite.delete_favorite(article_id, uid)
        if resp:
            article.modify(query={"favorite__gt": 0}, dec__favorite=1)


class ArticleRecommendApi(LoginView):
    def get(self):
        """
        
        @apiVersion 1.0.0
        @api {get} /api/recommend 简单返回推荐 
        @apiName ArticleRecommendApi
        @apiGroup plaza  
        
        @apiParam {Integer} page 第几页
        @apiParam {Integer} per_page 每页多少
        @apiSuccess {Integer} code 0
        
        @apiSuccessExample {json} Success-Response:
        {
            "code": 0,
            "articles": [
                {
                    "id": "asdfa",
                    "node": "asd",
                    "title": "a",
                    "comment": "a",
                    "top": true,
                    "time": 1233213213,
                    "click": 123,
                    "like": 32,
                    "favorite": true,
                    "who": 123,
                    "login": true,
                    "origin": true"
                },
                {
                    "id": "asdfa",
                    "node": "asd",
                    "title": "a",
                    "comment": "a",
                    "top": true,
                    "time": 1233213213,
                    "click": 123,
                    "like": 32,
                    "favorite": true,
                    "who": 123,
                    "login": true,
                    "origin": true"
                }
                ...
            ],
            "users": [
                {
                    "uid": 123,
                    "nickname": "asdf",
                    "role": 1,
                    "gender": 1,
                    "avatar": "www.ggadsf.com/asdfsafd.img",
                    "github": "github.com/adsfasdf",
                    "fp": true
                },
                {
                    "uid": 123,
                    "nickname": "asdf",
                    "role": 1,
                    "gender": 1,
                    "avatar": "www.ggadsf.com/asdfsafd.img",
                    "github": "github.com/adsfasdf",
                    "fp": true
                }
            ],
            "count": 123
            
        }
        """
        uid = g.uid
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)
        if page < 1: page = 1
        if per_page > 20: per_page = 20
        now = int(time.time())
        br_ins = BrowseRecord.search_uid(uid, 1, 10, now)  # 返回10条浏览记录
        nodes = {i.node for i in br_ins}
        # 返回此节点近一个星期的热点话题
        articles_list = []
        for node in nodes:
            articles = Article.search_week_hot(node, 1, 10)
            articles_list.extend(articles)
        articles_list.sort(key=operator.itemgetter("click"), reverse=True)
        articles = articles_list[(page - 1) * per_page:page * per_page]
        uids = {i.get("who") for i in articles}
        users = [User.with_id(uid).to_dict() for uid in uids]
        return {"articles": articles, "users": users, "count": len(articles_list)}


class ArticleCommentApi(ServiceView):
    def get(self, article_id):
        """
        
        @apiVersion 1.0.0
        @api {get} /api/comment/:article_id 获取评论 
        @apiName ArticleCommentApi
        @apiGroup plaza  
        
        @apiParam {String} article_id 文章ID
        @apiParam {Integer} page 第几页
        @apiParam {Integer} per_page 每页多少
        
        @apiSuccess {Integer} code 0
        
        @apiSuccessExample {json} Success-Response:
        {
            "comments": [
                {
                    content: "ghjk",
                    floor: 1,
                    id: "59769cd508ba1e382ca491f7",
                    rid: "596d5f6b5192000009e370f9",
                    time: 123123131,
                    uid: 123,
                    self: true
                }
                ...
            ],
            "users":[
                {
                    "uid": 123,
                    "nickname": "aa",
                    "role": 1,
                    "gender": 1,
                    "avatar": asd,
                    "github": github,
                    "fp": self.favorite_public
                }
            ],
            "count" : 21
        }
        
        """

        args = request.args
        page = args.get('page', default=1, type=int)
        per_page = args.get('per_page', default=10, type=int)
        if page <= 0: page = 1
        if per_page >= 20: per_page = 20
        parse_objectid(article_id)
        uid = g.uid
        result = {'comments': [], 'users': '', 'count': 0}
        uids = set()
        comments, count = ArticleComment.list_comment(article_id, page, per_page)
        result['count'] = count
        for comment in comments:
            payload = comment.to_dict()
            if comment.uid == uid:
                payload.update({"self": True})
                result['comments'].append(payload)
            else:
                payload.update({"self": False})
                result['comments'].append(payload)
            uids.add(comment.uid)
        users = [User.with_id(uid).to_dict() for uid in uids]
        result['users'] = users
        return result

    @login_required
    def post(self, article_id):
        """
        @apiVersion 1.0.0
        @api {post} /api/comment/:article_id 发表评论 
        @apiName ArticleCommentApiPost
        @apiGroup plaza  
        
        @apiParam {String} content 评论内容
        @apiParam {Integer} at @用户
        
        @apiSuccess {Integer} code 0
        
        @apiUse ArgsError
        @apiUse ArticleError
        @apiUse TokenRequired
        
         
        """
        data = request.form
        content = data.get('content')
        at = data.get('at', type=int, default=None)
        if len(content) > 300:
            raise ArgsError("评论字数最多300!")
        uid = g.uid
        parse_objectid(article_id)
        article = Article.with_id(article_id)
        if not article:
            raise ArticleError("文章没有找到!")
        article.modify(inc__comment=1)
        ArticleComment.create_comment(article_id, uid, article.comment, content)
        if at:  # 这里就不对相同用户进行屏蔽了
            # url : /article/595b053a08ba1e3064171e1e/595c8b4108ba1e1894cae48f
            Notification.create_notice("在文章{}第{}楼".format(article.title, article.comment), uid, at, content,
                                       "/article/{}/{}".format(str(article.node), str(article.pk)))

    @login_required
    def put(self, article_id, comment_id):
        """
        修改评论
        :param article_id:
         :param comment_id:
        :return: 
        """

    @login_required
    def delete(self, article_id, comment_id):
        """
        @apiVersion 1.0.0
        @api {delete} /api/comment/:article_id/:comment_id 删除评论 
        @apiName ArticleCommentApiDelet
        @apiGroup plaza  
        
        @apiParam {String} article_id 文章ID
        @apiParam {String} comment_id 评论ID
        
        @apiSuccess {Integer} code 0
        
        @apiUse CommentError
        @apiUse TokenRequired
        
        """
        parse_objectid(comment_id)
        comment = ArticleComment.with_id(comment_id)
        if not comment:
            raise CommentError("评论没有找到")
        uid = g.uid
        if uid == comment.uid:
            comment.delete()


class NoticePreApi(LoginView):
    def get(self):
        """
        @apiVersion 1.0.0
        @api {get} /api/message/new 预获取未读消息 
        @apiName NoticePreApi
        @apiGroup plaza  
        
        @apiSuccess {Integer} code 0
        @apiSuccessExample {json} Success-Response:
        {
            "code": 0,
            "count": 12
        }
        
        @apiUse TokenRequired
        
        """
        uid = g.uid
        count = Notification.objects(to=uid, status=NOTICE_STATUS["UNREAD"]).count()
        return {
            "count": count
        }


class NoticeApi(LoginView):
    def get(self):
        """
        @apiVersion 1.0.0
        @api {get} /api/message 获取未/已读消息 
        @apiName NoticeApi
        @apiGroup plaza  
      
        @apiParam {Integer} status 消息状态,1未读,2已读
        @apiParam {Integer} page 第几页
        @apiParam {Integer} per_page 每页多少
        
        @apiSuccess {Integer} code 0
        @apiSuccessExample {json} Success-Response:
        {
            "code": 0,
            "notification": [
                {
                    "desc": "[@root ](http://www.git-share.com/user/1)\n\n** test **",
                    "from": {
                        "avatar": "/static/public/avatar/12.png",
                        "fp": true,
                        "gender": null,
                        "github": "https://github.com/zonghow",
                        "nickname": "zonghow",
                        "role": 1,
                        "uid": 2
                    },
                    "id": "596c535d0adde8000974c235",
                    "status": 2,
                    "time": 1500271453,
                    "title": "在文章163FM第2楼",
                    "to": 1,
                    "url": "/article/596c417c65d44029759edcee/596c4dde43ac1700081b4098"
                }
            ]
        }
        
        @apiUse TokenRequired
        
        """
        # todo: 站内信功能的添加
        uid = g.uid
        args = request.args
        status = args.get('status', default=NOTICE_STATUS['UNREAD'], type=int)
        page = args.get('page', default=1, type=int)
        per_page = args.get('per_page', default=10, type=int)
        if page < 1: page = 1
        if per_page >= 20: per_page = 20
        ins = Notification.list_notice(uid, status, page, per_page)
        result = {"notification": [notice.to_dict() for notice in ins]}
        return result

    def put(self, notice_id):
        """
        @apiVersion 1.0.0
        @api {put} /api/message/:notice_id 修改消息状态 
        @apiName NoticeApi_put
        @apiGroup plaza  
        
        @apiParam notice_id 消息ID
        @apiParam status 消息状态
        
        @apiUse NotificationError
        @apiUse TokenRequired
        """
        parse_objectid(notice_id)
        status = request.form.get('status', default=NOTICE_STATUS["READ"], type=int)
        if status not in (NOTICE_STATUS["READ"], NOTICE_STATUS["DELETE"]):
            return
        ins = Notification.with_id(notice_id)
        if not ins:
            raise NotificationError("没有找到此通知!")
        if ins.to == g.uid:
            ins.modify({"status__ne": status}, set__status=status)

    def delete(self, notice_id):
        """
        @apiVersion 1.0.0
        @api {delete} /api/message/:notice_id 删除消息
        @apiName NoticeApi_Delete
        @apiGroup plaza  
        
        @apiParam notice_id 消息ID
        
        @apiUse NotificationError
        @apiUse TokenRequired
        """
        parse_objectid(notice_id)
        ins = Notification.with_id(notice_id)
        if not ins:
            raise NotificationError("没有找到此通知!")
        if ins.to == g.uid:
            ins.modify(set__status=NOTICE_STATUS['DELETE'])


class GitSpiderApi(ServiceView):
    @require_priv(2)
    def get(self, username):
        """
        @apiVersion 1.0.0
        @api {get} /api/repos/:username 获取github此<username>的所有公开的repos
        @apiName GitSpiderApi
        @apiGroup GitSpider
         
        @apiParam {String} username github用户名字
         
          
        """
        get_user_git.apply_async(args=[username])
