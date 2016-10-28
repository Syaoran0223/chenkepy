from app import db
from ._base import SessionMixin
from datetime import datetime

class InviteCode(db.Model, SessionMixin):
    __tablename__ = 'invite_code'

    def __init__(self, *args, **kwargs):
        InviteCode.register()
        super(InviteCode, self).__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    invite_code = db.Column(db.String(12))
    label = db.Column(db.String(20))
    state = db.Column(db.Integer)

    @staticmethod
    def get_code(invite_code):
        res = InviteCode.query.filter_by(state=1, invite_code=invite_code).first()
        return res is not None

    def __repr__(self):
        return '<Invite Code: %r>' % self.name


