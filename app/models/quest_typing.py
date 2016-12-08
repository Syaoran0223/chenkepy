from app import db
from ._base import SessionMixin
from app.utils import paginate
from app.const import EXAM_STATUS
from app.models import Question, Exam
import datetime
class QuestTyping(db.Model, SessionMixin):
    __tablename__ = 'quest_typing'

    def __init__(self, *args, **kwargs):
        QuestTyping.register()
        super(QuestTyping, self).__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer)
    quest_no = db.Column(db.Integer)
    quest_id= db.Column(db.Integer)
    state = db.Column(db.Integer)
    operator_id = db.Column(db.Integer)
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    def get_question_dtl(self):
        exam = Exam.query.get(self.exam_id)
        res = self.to_dict()
        res['exam'] = exam.get_dtl() if exam else {}
        return res
