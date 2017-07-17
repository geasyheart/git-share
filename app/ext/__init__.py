from app.ext import error_handler, error_logger, sentry_init


def configure(app):
    error_handler.configure(app)
    error_logger.configure(app)
    sentry_init.configure(app)
