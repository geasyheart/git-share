from app.models.feedback.model import FeedbackLimit, Feedback
from tests.base import MetaTest


class FeedbackTest(MetaTest):
    def ensure_db(self):
        FeedbackLimit.drop_collection()
        Feedback.drop_collection()

    def test_model(self):
        """
        测试模型
        :return:
        """
        uid1, uid2 = 11, 22
        for i in range(5):
            for uid in (uid1, uid2):
                b = FeedbackLimit.create_limit(uid)
                self.assertEqual(b, 1)
        for i in range(10):
            for uid in (uid1, uid2):
                b = FeedbackLimit.create_limit(uid)
                self.assertEqual(b, 0)
        for i in range(100):
            Feedback.create_feedback(1, "1233213131312")
            Feedback.create_feedback(2, "1233213131312")
            Feedback.create_feedback(3, "1233213131312")
        self.assertEqual(Feedback.objects.count(), 300)

    def test_api(self):
        """
        测试api
        :return:
        """
        pass
