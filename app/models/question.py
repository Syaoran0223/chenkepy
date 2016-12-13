from app import db
from app.const import EXAM_STATUS,QUEST_STATUS
from app.utils import pagination
from ._base import SessionMixin
from .quest_review_log import QuestReviewLog
from .questLog import QuestLog
from .exam import Exam
from .schools import School

class Question(db.Model, SessionMixin):
    __tablename__ = 'quest'

    def __init__(self, *args, **kwargs):
        Question.register()
        super(Question, self).__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    has_sub = db.Column(db.Integer, default=0)
    exam_id = db.Column(db.Integer)
    quest_type_id = db.Column(db.Integer)
    quest_image =  db.Column(db.JsonBlob(), default=[])
    answer_image =  db.Column(db.JsonBlob(), default=[])
    quest_no = db.Column(db.Integer)
    quest_content = db.Column(db.String(1000))
    quest_content_html = db.Column(db.String(1000))
    option_count = db.Column(db.Integer)
    qrows = db.Column(db.Integer)
    qcols = db.Column(db.Integer)
    kaodian = db.Column(db.String(255))
    fenxi = db.Column(db.String(255))
    jieda = db.Column(db.String(255))
    correct_answer = db.Column(db.String(255))
    knowledge_point = db.Column(db.String(255))
    state = db.Column(db.Integer)
    insert_user_id = db.Column(db.Integer)
    
    def __repr__(self):
        return '<Question: %r>' % self.id

    def get_dtl(self):
        exam = Exam.query.get(self.exam_id)
        exam_dict = exam.to_dict() if exam else {}
        exam_dict = School.bind_auto(exam_dict, 'name')
        res = self.to_dict()
        res['exam'] = exam_dict
        return res

    @staticmethod
    def add_pre_process_quest(exam_id, quest_no,has_sub, quest_type_id, option_count, quest_image, user_id, review_memo, answer_image):
        quest = Question(exam_id=exam_id, quest_no=quest_no,
            has_sub=has_sub, quest_type_id=quest_type_id,
            option_count=option_count, quest_image=quest_image,
            answer_image=answer_image, state=QUEST_STATUS['未处理'],
            insert_user_id=user_id)
        quest.save()

        res = Question.query.get(quest.id)
        return res.to_dict()

    @staticmethod
    def get_quest_by_state(state):
        query = Question.query.filter_by(state=state).\
            order_by(Question.created_at.desc())
        res = pagination(query)
        items = res.get('items',[])
        items = Exam.bind_auto(items,['name', 'year', 'school_id', 'section', 'subject', 'grade'])
        items = School.bind_auto(items, 'name', 'exam_school_id')
        res['items'] = items
        return res