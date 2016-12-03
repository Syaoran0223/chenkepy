from app import db
from ._base import SessionMixin
from app.utils import paginate
from app.const import EXAM_STATUS
from app.models import Exam, Region, School, User
import datetime
class QuestLog(db.Model, SessionMixin):
    __tablename__ = 'quest_log'

    def __init__(self, *args, **kwargs):
        QuestLog.register()
        super(QuestLog, self).__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer)
    quest_no = db.Column(db.Integer)
    refer_user_id = db.Column(db.Integer)
    log_state = db.Column(db.Integer)
    log_type = db.Column(db.String(32))
