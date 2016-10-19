from app import db
from ._base import SessionMixin

class School(db.Model, SessionMixin):
    __tablename__ = 'school'

    id = db.Column(db.Integer, primary_key=True)
    ctid = db.Column(db.Integer)
    type = db.Column(db.Integer)
    name = db.Column(db.String(30))

    @staticmethod
    def get_schools_by_ctid(ctid):
        res = School.query.filter_by(ctid=ctid).all()
        res = list(map(lambda x: x.to_dict(), res))
        return res
    

    def __repr__(self):
        return '<Region: %r>' % self.name
