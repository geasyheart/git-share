import logging
from logging.handlers import RotatingFileHandler


def configure(app):
    error_log_enable = app.config.get('ERRORLOG_ENABLE', True)
    if not error_log_enable:
        return
    err_path = app.config.get('ERRORLOG_FILE', 'logs/error.log')
    handler = RotatingFileHandler(
        filename=err_path,
        maxBytes=500 * 1024,
        backupCount=10
    )
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
