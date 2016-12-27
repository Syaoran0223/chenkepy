from app import db
from ._base import SessionMixin

class QOption(db.Model, SessionMixin):
    __tablename__ = 'qoption'
    def __init__(self, *args, **kwargs):
        QOption.register()
        super(QOption, self).__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    qid = db.Column(db.Integer)
    qok = db.Column(db.Boolean, default=False)
    qsn = db.Column(db.String(16))
    qopt = db.Column(db.Text)

    def __repr__(self):
        return '<QOption: %r>' % self.id