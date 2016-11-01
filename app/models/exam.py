from app import db
from ._base import SessionMixin
from config import Config
from app.utils import pagination
from . import School
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
        query = db.session.query(Exam, School).filter_by(upload_user=upload_user).order_by(Exam.created_at.desc(), Exam.state)
        query = query.join(School, Exam.school_id == School.id)

        return pagination(query)

    @staticmethod
    def get_exam(id):
        return Exam.query.get(int(id))

    def __repr__(self):
        return '<Exam: %r>' % self.name
