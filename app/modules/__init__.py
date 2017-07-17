import os
from importlib import import_module


def register_route(app):
    """
    注册路由..
    :param app: 
    :return: 
    """
    project_path = app.config['PROJECT_PATH']
    modules_path = os.path.join(project_path, 'modules')
    dirs = (_dir for _dir in os.listdir(modules_path) if os.path.isdir(os.path.join(modules_path, _dir)))
    for _dir in dirs:
        files = os.listdir(os.path.join(modules_path, _dir))
        if 'urls.py' not in files:
            continue
        module_path = 'app.modules.{}.urls'.format(_dir)
        urls_attr = import_module(module_path)
        if hasattr(urls_attr, 'modules'):
            blueprint = getattr(urls_attr, 'modules')
            # 此处添加api前缀
            # app.register_blueprint(blueprint=blueprint, url_prefix="/api")
            app.register_blueprint(blueprint=blueprint)
