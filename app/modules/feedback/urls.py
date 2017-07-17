from flask import Blueprint

from app.modules.feedback.apis import FeedbackApi

modules = Blueprint("feedback", __name__, url_prefix="/api")

modules.add_url_rule("/feedback", view_func=FeedbackApi.as_view("feedback_api"), methods=['POST'])
