from app import db
from ._base import SessionMixin
from app.utils import paginate
from app.const import EXAM_STATUS
from app.models import Exam, Region, School, User
import datetime
class ExamLog(db.Model, SessionMixin):
    __tablename__ = 'exam_log'

    def __init__(self, *args, **kwargs):
        ExamLog.register()
        super(ExamLog, self).__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer)
    refer_user_id = db.Column(db.Integer)
    log_state = db.Column(db.Integer)
    log_type = db.Column(db.String(32))

    @staticmethod
    def log(exam_id, refer_user_id, log_state, log_type):
        log = ExamLog(exam_id=exam_id,
            refer_user_id=refer_user_id, log_state=log_state,
            log_type=log_type)
        log.save()