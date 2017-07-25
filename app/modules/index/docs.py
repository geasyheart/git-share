import os

from app.core.kit import ServiceView
from flask import send_from_directory, current_app


class DocsView(ServiceView):
    def get(self, path):
        """
        more : http://apidocjs.com/#param-api-error
        :param path: 
        :return: 
        """
        if current_app.config["MODE"] == "DEV":
            if path.startswith("index.html"):
                os.system('apidoc -i app/ -o docs/')
            return send_from_directory("../docs/", path)
