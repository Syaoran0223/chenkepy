from app import db
from ._base import SessionMixin
from sqlalchemy import text
import enum


class Message(db.Model, SessionMixin):
    __tablename__ = 'message'

    def __init__(self, *args, **kwargs):
        Message.register()
        super(Message, self).__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    type = db.Column(db.Enum('TYPE_SCORE'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Message: %r>' % self.title

    @staticmethod
    def set_is_read(message_ids):
        message_ids = ','.join(message_ids)
        sql = text('update message set is_read=1 where id in ({})'.format(message_ids))
        db.engine.execute(sql)
        
