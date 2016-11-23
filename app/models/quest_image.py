from app import db
from ._base import SessionMixin
from app.utils import pagination
from const import QUEST_IMAGE_STATUS
import datetime
class QuestImage(db.Model, SessionMixin):
    __tablename__ = 'quest_image'

    def __init__(self, *args, **kwargs):
        QuestImage.register()
        super(QuestImage, self).__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer)
    have_sub = db.Column(db.Integer)
    quest_no = db.Column(db.String(3))
    quest_type = db.Column(db.Integer)
    quest_option_count = db.Column(db.Integer)
    quest_image = db.Column(db.LargeBinary)
    quest_answer_image = db.Column(db.LargeBinary)
    add_user = db.Column(db.Integer)
    review_state = db.Column(db.Integer)


    @staticmethod
    def list_image(state=QUEST_IMAGE_STATUS['未处理']):
        res = pagination(QuestImage.query.filter(QuestImage.review_state == state).order_by(QuestImage.id,QuestImage.quest_no))
        return res

    def view_quest_image_detail(quest_no = 0):
        return QuestImage.query.filter(QuestImage.quest_no==quest_no)
