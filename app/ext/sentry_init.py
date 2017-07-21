from raven.contrib.flask import Sentry

sentry = Sentry()


def configure(app):
    dsn = app.config['SENTRY_DSN']
    if app.config.get("MODE") == "DEV":
        return
    sentry.init_app(app, dsn)
