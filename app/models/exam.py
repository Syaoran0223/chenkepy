from app import db
from ._base import SessionMixin
from app.utils import pagination
from app.models import School, Region
from app.const import EXAM_STATUS
import datetime
class Exam(db.Model, SessionMixin):
    __tablename__ = 'exam'

    def __init__(self, *args, **kwargs):
        Exam.register()
        super(Exam, self).__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    section = db.Column(db.String(12))
    subject = db.Column(db.String(5))
    paper_types = db.Column(db.String(17))
    province_id = db.Column(db.Integer)
    city_id = db.Column(db.Integer)
    area_id = db.Column(db.Integer)
    school_id = db.Column(db.Integer)
    year = db.Column(db.Integer)
    grade = db.Column(db.Integer)
    state = db.Column(db.Integer)
    upload_user = db.Column(db.Integer)
    attachments = db.Column(db.JsonBlob(), default=[])
    review_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    def get_dtl(self):
        result = {
            'id': self.id,
            'name': self.name,
            'sections': self.section,
            'subject': self.subject,
            'paper_types': self.paper_types,
            'province_id': self.province_id,
            'city_id': self.city_id,
            'area_id': self.area_id,
            'school_id': self.school_id,
            'year': self.year,
            'grade': self.grade,
            'state': self.state,
            'upload_user': self.upload_user,
            'attachments': self.attachments,
            'review_date': self.review_date.strftime('%Y-%m-%d %H:%M:%S')
        }
        result = Region.bind_auto(result, 'name', 'city_id', 'id', 'city')
        result = Region.bind_auto(result, 'name', 'province_id', 'id', 'province')
        result = Region.bind_auto(result, 'name', 'area_id', 'id', 'area')
        result = School.bind_auto(result, 'name', 'school_id', 'id', 'school')
        return result

    @staticmethod
    def get_exams(upload_user):
        #查询上传用户试卷记录
        res = pagination(Exam.query.filter(Exam.upload_user == upload_user, Exam.state >= EXAM_STATUS['审核不通过']).order_by(Exam.created_at.desc(), Exam.state))
        items = res.get('items', [])
        items = School.bind_auto(items, 'name')
        res['items'] = items
        return res

    def xlist_exams(state= 0,userid=0):
        res = pagination(Exam.query.filter(Exam.state == state ,Exam.upload_user!=userid).order_by(Exam.created_at.desc()))
        items = res.get('items', [])
        items = School.bind_auto(items, 'name')
        res['items'] = items
        return res

    def list_exams(state=EXAM_STATUS['已审核'] ):
        res = pagination(Exam.query.filter(Exam.state == state).order_by(Exam.created_at.desc()))
        items = res.get('items',[])
        items = School.bind_auto(items,'name')
        res['items'] = items
        return res

    @staticmethod
    def get_exam(id):
        result = Exam.query.get(int(id))
        if result is not None:
            result = result.to_dict()
        else:
            return None
        result = Region.bind_auto(result, 'name', 'city_id', 'id', 'city')
        result = Region.bind_auto(result, 'name', 'province_id', 'id', 'province')
        result = Region.bind_auto(result, 'name', 'area_id', 'id', 'area')
        result = School.bind_auto(result, 'name', 'school_id', 'id', 'school')

        return result

    def __repr__(self):
        return '<Exam: %r>' % self.name
