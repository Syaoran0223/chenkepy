from app import db
from ._base import SessionMixin

class QType(db.Model, SessionMixin):
    __tablename__ = 'qtype'
    def __init__(self, *args, **kwargs):
        QType.register()
        super(QType, self).__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer)
    name = db.Column(db.String(60))
    category = db.Column(db.Integer)
    parent_id = db.Column(db.Integer)
    orderid = db.Column(db.Integer)

    def __repr__(self):
        return '<SubQuestion: %r>' % self.id

    def list_type(subject_id=0):
        return QType.query.filter_by(subject_id=subject_id).order_by(QType.orderid).all()