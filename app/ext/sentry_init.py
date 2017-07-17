from raven.contrib.flask import Sentry

sentry = Sentry()


def configure(app):
    dsn = app.config['SENTRY_DSN']
    sentry.init_app(app, dsn)
