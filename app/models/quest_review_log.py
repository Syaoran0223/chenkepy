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

    @staticmethod
    def list_log(reviewer_id, pageIndex=1, pageSize=20):
        from .question import Question
        # 查询上传用户试卷记录
        result = db.session.query(Question, QuestReviewLog, User).filter(Question.id == QuestReviewLog.exam_id,
                                                                                 QuestReviewLog.reviewer_id == reviewer_id,
                                                                                 QuestReviewLog.review_state != EXAM_STATUS[
                                                                                '未审核'] and QuestReviewLog.review_state !=
                                                                            EXAM_STATUS[
                                                                                '已删除'] and QuestReviewLog.reviewer_id == User.id).order_by(
            QuestReviewLog.review_date.desc())
        result = paginate(result, pageIndex, pageSize, error_out=False)
        items = []
        for item in result.items:
            obj = {
                'id': item.QuestReviewLog.id,
                'quest_content': item.Question.quest_content_html,
                'quest_no': item.Question.quest_no,
                'reviewer': item.User.name,
                'review_state': item.QuestReviewLog.review_state,
                'review_date': item.QuestReviewLog.review_date.strftime("%Y-%m-%d %H:%M:%S"),
                'review_memo': item.QuestReviewLog.review_memo
            }
            items.append(obj)

        res = {
            'items': items,
            'pageIndex': result.page - 1,
            'pageSize': result.per_page,
            'totalCount': result.total,
            'totalPage': result.pages
        }
        return res