from app import db
from ._base import SessionMixin
from datetime import datetime

class InviteCode(db.Model, SessionMixin):
    __tablename__ = 'invite_code'

    id = db.Column(db.Integer, primary_key=True)
    invite_code = db.Column(db.String(12))
    label = db.Column(db.String(20))
    state = db.Column(db.Integer)
    add_time = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Invite Code: %r>' % self.name
