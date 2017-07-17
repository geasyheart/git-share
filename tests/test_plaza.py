from app.models.accounts.users import User
from app.models.plaza.article import ArticleNode, Article
from tests.base import MetaTest


class PlazaTest(MetaTest):
    def ensure_db(self):
        ArticleNode.drop_collection()
        Article.drop_collection()
        User.drop_collection()

    # def test_node(self):
    #     ArticleNode.create_node("编程")
    #     ArticleNode.create_node("Python")
    #     ArticleNode.create_node("GOlang")
    #     resp = self.get("/api/node")
    #     node = resp.get('node')
    #     self.assertEqual(len(node), 3)
    #     ArticleNode.create_node("GOlang")
    #     resp = self.get("/api/node")
    #     node = resp.get('node')
    #     self.assertEqual(len(node), 3)
    #     ArticleNode.create_node("GOLang")
    #     resp = self.get("/api/node")
    #     node = resp.get('node')
    #     self.assertEqual(len(node), 4)

    def test_recommend(self):
        user = User.signup("110@qq.com",'abcd1234',"haha")
        ins = ArticleNode.create_node("Python")
        node1 = ins.pk
        ins = ArticleNode.create_node("Golang")
        node2 = ins.pk
        for i in range(10):
            Article.create_article("node1-{}".format(i), None, node1,user.uid, True)
            Article.create_article("node2-{}".format(i), None, node2,user.uid, True)

