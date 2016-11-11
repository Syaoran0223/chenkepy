from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from flask.ext.login import UserMixin, AnonymousUserMixin
from app import db, login_manager
from ._base import SessionMixin

class User(db.Model, SessionMixin, UserMixin):
    __tablename__ = 'user'
    protected_field = ['password_hash', 'last_login_ip', 'code']

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
    scores = db.relationship('Score', backref='user',
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
    

    def __repr__(self):
        return '<User: %r>' % self.name

class AnonymousUser(AnonymousUserMixin):
    def is_admin(self):
        return False

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

login_manager.anonymous_user = AnonymousUser