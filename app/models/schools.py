from app import db
from ._base import SessionMixin

class School(db.Model, SessionMixin):
    __tablename__ = 'school'

    def __init__(self, *args, **kwargs):
        School.register()
        super(School, self).__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    ctid = db.Column(db.Integer)
    type = db.Column(db.Integer)
    name = db.Column(db.String(30))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'title': self.name
        }

    @staticmethod
    def get_schools_by_ctid(ctid, title=""):
        query = School.query.filter_by(ctid=ctid)
        if title:
            query = query.filter(School.name.like('%{}%'.format(title)))
        res = query.all()
        res = list(map(lambda x: x.to_dict(), res))
        return res
    

    def __repr__(self):
        return '<Region: %r>' % self.name
