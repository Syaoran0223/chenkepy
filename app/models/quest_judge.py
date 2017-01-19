from app import db
from ._base import SessionMixin
from app.utils import paginate
from app.const import EXAM_STATUS
from app.models import Question, Exam
import datetime
class QuestJudge(db.Model, SessionMixin):
    __tablename__ = 'quest_judge'

    def __init__(self, *args, **kwargs):
        QuestJudge.register()
        super(QuestJudge, self).__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer)
    quest_no = db.Column(db.Integer)
    quest_id= db.Column(db.Integer)
    state = db.Column(db.Integer)
    operator_id = db.Column(db.Integer)
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    def get_question_dtl(self):
        res = self.to_dict()
        question = Question.query.get(self.quest_id)
        res['question'] = question.to_dict()
        return res
