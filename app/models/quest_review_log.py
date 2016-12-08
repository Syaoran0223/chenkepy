from app import db
from ._base import SessionMixin
from app.utils import paginate
from app.const import EXAM_STATUS
from .users import User
import datetime

class QuestReviewLog(db.Model, SessionMixin):
    __tablename__ = 'quest_review_log'

    def __init__(self, *args, **kwargs):
        QuestReviewLog.register()
        super(QuestReviewLog, self).__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer)
    quest_no = db.Column(db.Integer)
    reviewer_id = db.Column(db.Integer)
    review_state = db.Column(db.Integer)
    review_memo = db.Column(db.String(100))
    review_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())