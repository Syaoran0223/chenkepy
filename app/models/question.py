from app import db
from app.const import EXAM_STATUS
from app.utils import pagination
from ._base import SessionMixin
from .quest_review_log import QuestReviewLog

class Question(db.Model, SessionMixin):
    __tablename__ = 'quest'

    def __init__(self, *args, **kwargs):
        Question.register()
        super(Question, self).__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    has_sub = db.Column(db.Boolean, default=False)
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
    state = db.Column(db.String(255))
    
    def __repr__(self):
        return '<Question: %r>' % self.id

    # @staticmethod
    # def list_image(state=EXAM_STATUS['未处理']):
    #     res = pagination(Question.query.filter(Question.review_state == state).order_by(Question.id,Question.quest_no))
    #     return res

    @staticmethod
    def view_quest_detail(id=0):
        return Question.query.filter(Question.id==id).all()

    @staticmethod
    def add_pre_process_image(exam_id, quest_no,has_sub, quest_type_id, option_count, quest_image, user_id, review_memo, answer_image):
        quest = Question(exam_id=exam_id, quest_no=quest_no,has_sub=has_sub, quest_type_id=quest_type_id, option_count=option_count, quest_image=quest_image,answer_image=answer_image, state=EXAM_STATUS['预处理完成'])
        quest.save()
        quest_review_log = QuestReviewLog(exam_id=exam_id, quest_no=quest_no, reviewer_id=user_id, review_state=EXAM_STATUS['预处理完成'], review_memo=review_memo)
        quest_review_log.save()
        res = Question.query.get(quest.id)
        return res.to_dict()
