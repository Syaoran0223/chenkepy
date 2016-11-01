from app import db
from ._base import SessionMixin
from app.utils import pagination
from app.models import School, Region

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

    @staticmethod
    def get_exams(upload_user):
        res = pagination(Exam.query.filter_by(upload_user=upload_user).order_by(Exam.created_at.desc(), Exam.state))
        items = res.get('items', [])
        items = School.bind_auto(items, 'name')
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
