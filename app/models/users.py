from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from flask.ext.login import UserMixin, AnonymousUserMixin
from app import db, login_manager
from app.models.permissions import Permission
from ._base import SessionMixin
from app.models.regions import Region
from app.models.schools import School

class User(db.Model, SessionMixin, UserMixin):
    __tablename__ = 'user'
    protected_field = ['password','password_hash', 'last_login_ip', 'code']
    search_fields = ['name_like',
        'phone_like', 'state', 'created_at_begin',
        'created_at_end', 'school_id', 'grade_id',
        'city_id', 'province_id', 'area_id',
        'permissions_like']

    def __init__(self, *args, **kwargs):
        User.register()
        super(User, self).__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    school_id = db.Column(db.Integer)
    grade_id = db.Column(db.Integer)
    city_id = db.Column(db.Integer)
    province_id = db.Column(db.Integer)
    area_id = db.Column(db.Integer)
    user_type = db.Column(db.Integer)
    last_login_ip = db.Column(db.String(64))
    state = db.Column(db.Integer, default=0)
    phone = db.Column(db.String(16))
    code = db.Column(db.String(12))
    permissions = db.Column(db.JsonBlob(), default=[])
    scores = db.relationship('Score', backref='user',
                                lazy='dynamic')
    messages = db.relationship('Message', backref='user',
                                lazy='dynamic')

    @property
    def password(self):
        return AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def get_menus(self):
        permissions = self.permissions
        menus = []
        for p in permissions:
            menus += Permission.__dict__.get(p, [])
        return [{'identity': m} for m in menus]

    def to_dict(self):
        res = super(User, self).to_dict()
        res = Region.bind_auto(res, 'name', 'province_id', 'id', 'province')
        res = Region.bind_auto(res, 'name', 'city_id', 'id', 'city')
        res = Region.bind_auto(res, 'name', 'area_id', 'id', 'area')
        res = School.bind_auto(res, 'name', 'school_id', 'id', 'school')
        return res

    def get_admin_summary(self, begin_time, end_time):
        sql = '''select
                    sum(case when state=0 then 1 else 0 end) as ready,
                    sum(case when state=1 then 1 else 0 end) as confirming,
                    sum(case when state=5 then 1 else 0 end) as pass,
                    sum(case when state>=2 and state <=4 then 1 else 0 end) as useage
                from `exam`
                where upload_user=2
                and created_at >= %s and created_at <= %s;'''


    

    def __repr__(self):
        return '<User: %r>' % self.name

class AnonymousUser(AnonymousUserMixin):
    def is_admin(self):
        return False

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

login_manager.anonymous_user = AnonymousUser