from app import db
from ._base import SessionMixin

class Region(db.Model, SessionMixin):
    __tablename__ = 'region'

    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)
    type = db.Column(db.Integer)
    code = db.Column(db.String(6))
    name = db.Column(db.String(30))

    @staticmethod
    def get_province():
        res = Region.query.filter_by(type=0).all()
        res = list(map(lambda x: x.to_dict(), res))
        return res

    @staticmethod
    def get_city(pro_id):
        res = Region.query.filter_by(type=1, pid=pro_id).all()
        res = list(map(lambda x: x.to_dict(), res))
        return res

    @staticmethod
    def get_area(city_id):
        res = Region.query.filter_by(type=2, pid=city_id).all()
        res = list(map(lambda x: x.to_dict(), res))
        return res
    

    def __repr__(self):
        return '<Region: %r>' % self.name
