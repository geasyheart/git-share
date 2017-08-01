from flask import jsonify


def configure(app):
    @app.errorhandler(401)
    def forbidden_page(*args, **kwargs):
        """
        返回401错误信息
        :param args:
        :param kwargs:
        :return:
        """
        return jsonify({"code": 401, "message": "Not allowed"})

    @app.errorhandler(403)
    def forbidden_page(*args, **kwargs):
        """
        返回403错误信息
        :param args:
        :param kwargs:
        :return:
        """
        return jsonify({"code": 403, "message": "Not allowed"})

    @app.errorhandler(404)
    def notfound_page(*args, **kwargs):
        """
        返回404错误信息
        :param args:
        :param kwargs:
        :return:
        """
        return jsonify({"code": 404, "message": "Not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(*args, **kwargs):
        """
        返回405错误信息
        :param args:
        :param kwargs:
        :return:
        """
        return jsonify({"code": 405, "message": "method not allowed!"})

    @app.errorhandler(500)
    def server_error(*args, **kwargs):
        """
        返回500错误信息
        :param args:
        :param kwargs:
        :return:
        """

        return jsonify({"code": 500, "message": "server BUG!"})
