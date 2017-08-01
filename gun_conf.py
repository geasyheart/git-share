from multiprocessing import cpu_count
from os import environ, path

_host = environ.get('GH_HOST', '0.0.0.0')
_port = environ.get('GH_PORT', 80)

bind = "{}:{}".format(_host, str(_port))

workers = environ.get('GH_WORKERS', cpu_count() * 2 + 1)

access_log_format = "%({X-Real-IP}i)s %(h)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s"
accesslog = path.join(environ.get('GH_LOGS_DIR', '/logs/'), 'access.log')
errorlog = path.join(environ.get('GH_LOGS_DIR', '/logs/'), 'error.log')
