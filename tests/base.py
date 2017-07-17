import json
from unittest import TestCase
from app import create_app


class MetaTest(TestCase):
    app = None

    def setUp(self):
        self.app = create_app(test=True)
        self.ensure_db()
        self.client = self.app.test_client(use_cookies=True)

    def ensure_db(self):
        pass

    def send_request(self, *args, **kwargs):
        """
            由于服务器端设置成自动接收form或json数据,所以这个地方就默认以data={}的形式进行发送，而不是
            json格式的数据
        :param args
        :param kwargs:
        :return:

        ('/url',data={},json={})
        """

        if 'json' in kwargs:
            kwargs.setdefault('data', json.dumps(kwargs.get('json')))
            kwargs.setdefault('content_type', 'application/json')
            kwargs.pop('json')
        if 'param' in kwargs:
            kwargs.setdefault('query_string', kwargs.get('param'))
            kwargs.pop('param')
        resp = self.client.open(*args, **kwargs)
        data = resp.data.decode("utf-8")
        d = json.loads(data)
        return d

    def get(self, *args, **kwargs):
        return self.send_request(method="GET", *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.send_request(method="POST", *args, **kwargs)

    def put(self, *args, **kwargs):
        return self.send_request(method="PUT", *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.send_request(method="PATCH", *args, **kwargs)

    def copy(self, *args, **kwargs):
        return self.send_request(method="COPY", *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.send_request(method="DELETE", *args, **kwargs)
