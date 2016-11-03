from app import db
from ._base import SessionMixin

class ExamReviewLog(db.Model, SessionMixin):
    __tablename__ = 'exam_review_log'

    def __init__(self, *args, **kwargs):
        ExamReviewLog.register()
        super(ExamReviewLog, self).__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer)
    review_id = db.Column(db.Integer)
    review_state = db.Column(db.Integer)
    review_memo = db.Column(db.String(100))

    @staticmethod
    def list_log():
        return None
