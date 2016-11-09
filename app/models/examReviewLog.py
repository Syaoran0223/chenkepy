from app import db
from ._base import SessionMixin
from app.utils import paginate
from app.const import EXAM_STATUS
from app.models import Exam, Region, School, User
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
        result = db.session.query(Exam, ExamReviewLog, School, User).filter(Exam.id == ExamReviewLog.exam_id, ExamReviewLog.reviewer_id == reviewer_id,ExamReviewLog.review_state!=EXAM_STATUS['未审核'] and ExamReviewLog.review_state!=EXAM_STATUS['已删除'] and Exam.school_id == School.id and ExamReviewLog.reviewer_id == User.id).order_by(ExamReviewLog.review_date.desc())
        result = paginate(result, pageIndex, pageSize, error_out=False)
        items = []
        for item in result.items:
            obj = {
                'id':item.ExamReviewLog.id,
                'name':item.Exam.name,
                'shool_name':item.School.name,
                'section':item.Exam.section,
                'year':item.Exam.year,
                'grade':item.Exam.grade,
                'subject':item.Exam.subject,
                'reviewer':item.User.name,
                'review_state':item.ExamReviewLog.review_state,
                'review_date':item.ExamReviewLog.review_date.strftime("%Y-%m-%d %H:%M:%S"),
                'review_memo':item.ExamReviewLog.review_memo
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