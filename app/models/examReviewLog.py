from app import db
from ._base import SessionMixin
from app.utils import paginate
from app.const import EXAM_STATUS
from app.models import Exam
import datetime
class ExamReviewLog(db.Model, SessionMixin):
    __tablename__ = 'exam_review_log'

    def __init__(self, *args, **kwargs):
        ExamReviewLog.register()
        super(ExamReviewLog, self).__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer)
    reviewer_id = db.Column(db.Integer)
    review_state = db.Column(db.Integer)
    review_memo = db.Column(db.String(100))
    review_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    @staticmethod
    def list_log(reviewer_id, pageIndex=1, pageSize = 20):
        # 查询上传用户试卷记录
        result = db.session.query(Exam, ExamReviewLog).filter(Exam.id == ExamReviewLog.exam_id, ExamReviewLog.reviewer_id == reviewer_id,ExamReviewLog.review_state!=EXAM_STATUS['未审核'] and ExamReviewLog.review_state!=EXAM_STATUS['已删除']).order_by(ExamReviewLog.updated_at.desc())
        result = paginate(result, pageIndex, pageSize, error_out=False)
        #result = pagination(ExamReviewLog.query.filter(ExamReviewLog.reviewer_id == reviewer_id, ExamReviewLog.review_state >= EXAM_STATUS['审核不通过']).order_by(ExamReviewLog.updated_at.desc()))
        items = result.items
        res = {
            'items': items,
            'pageIndex': data.page - 1,
            'pageSize': data.per_page,
            'totalCount': data.total,
            'totalPage': data.pages
        }
        return res
        return items