from app import db
from ._base import SessionMixin
from datetime import datetime
from . import Attachment
from config import Config
class Exam(db.Model, SessionMixin):
    __tablename__ = 'exam'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    section = db.Column(db.String(12))
    subject = db.Column(db.String(5))
    paper_types = db.Column(db.String(17))
    province_id = db.Column(db.String(6))
    city_id = db.Column(db.String(6))
    area_id = db.Column(db.String(6))
    school_id = db.Column(db.String(8))
    year = db.Column(db.String(4))
    grade = db.Column(db.Integer)
    state = db.Column(db.Integer)
    attachments = db.relationship('Attachment', backref='exam', lazy='dynamic')
    add_time = db.Column(db.DateTime, default=datetime.now)

    @staticmethod
    def get_exams(pageindex):
        return Exam.query.order_by(Exam.add_time.desc()).paginate(pageindex, per_page=Config.PER_PAGE, error_out=False)

    def __repr__(self):
        return '<Exam: %r>' % self.name