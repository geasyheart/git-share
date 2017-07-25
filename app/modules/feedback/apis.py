from flask import g, request

from app.core.exception import ArgsError
from app.core.kit import LoginView
from app.models.feedback.model import Feedback, FeedbackLimit


class FeedbackApi(LoginView):
    def post(self):
        """
        @apiVersion 1.0.0
        @api {post} /api/feedback 反馈 
        @apiName FeedbackApi
        @apiGroup Feedback
        
        @apiParam {String} content 反馈内容
        
        @apiSuccess {Integer} code 0
        @apiUse ArgsError
        """
        content = request.form.get('content')
        uid = g.uid
        if not content:
            raise ArgsError("需要输入反馈~")
        if content and len(content) > 1000:
            raise ArgsError("反馈内容太长~")
        b = FeedbackLimit.create_limit(uid)
        if b:
            Feedback.create_feedback(uid, content)
