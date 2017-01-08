from app import db
from ._base import SessionMixin
import datetime

class Preprocess(db.Model, SessionMixin):
    __tablename__ = 'pre_process'

    def __init__(self, *args, **kwargs):
        Preprocess.register()
        super(Preprocess, self).__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer)
    operator_id = db.Column(db.Integer)
    state = db.Column(db.Integer)
    memo = db.Column(db.String(100))
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)