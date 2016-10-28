#coding: utf-8

from app import db
from app.models._base import SessionMixin
from datetime import datetime

class Attachment(db.Model, SessionMixin):
    __tablename__ = 'attachments'

    def __init__(self, *args, **kwargs):
        Attachment.register()
        super(Attachment, self).__init__(*args, **kwargs)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=True, default='')
    url = db.Column(db.String(128))
    file_type = db.Column(db.String(128)) # 本地路径
    user_id = db.Column(db.Integer)

    @staticmethod
    def get_attachment(att_id):
        return Attachment.query.get(int(att_id))