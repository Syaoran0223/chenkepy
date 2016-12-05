from app import db
from ._base import SessionMixin
from app.utils import paginate
from app.const import EXAM_STATUS
from app.models import Exam, Region, School, User
import datetime
class QuestTyping(db.Model, SessionMixin):
    __tablename__ = 'quest_typing'

    def __init__(self, *args, **kwargs):
        QuestTyping.register()
        super(QuestTyping, self).__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer)
    quest_no = db.Column(db.Integer)

    oper_id = db.Column(db.Integer)
    oper_state = db.Column(db.Integer)
    oper_memo = db.Column(db.String(100))
    oper_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
