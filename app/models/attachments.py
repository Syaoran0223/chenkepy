#coding: utf-8

from app import db
from app.models._base import SessionMixin
from datetime import datetime

class Attachment(db.Model, SessionMixin):
    __tablename__ = 'attachments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=True, default='')
    url = db.Column(db.String(128))
    file_type = db.Column(db.String(128)) # 本地路径
    user_id = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.now)
   # exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'))

    @staticmethod
    def get_attachment(att_id):
        return Attachment.query.get(int(att_id))