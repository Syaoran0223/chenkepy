from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db, login_manager_admin
from flask.ext.login import UserMixin, AnonymousUserMixin
from app import db
from ._base import SessionMixin

class Admin(db.Model, SessionMixin, UserMixin):
    __tablename__ = 'admin'
    protected_field = ['password','password_hash', 'last_login_ip']

    def __init__(self, *args, **kwargs):
        Admin.register()
        super(User, self).__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    last_login_ip = db.Column(db.String(64))
    state = db.Column(db.Integer, default=0)
    phone = db.Column(db.String(16))

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
        return '<Admin: %r>' % self.name

class AnonymousUser(AnonymousUserMixin):
    def is_admin(self):
        return False

@login_manager_admin.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

login_manager_admin.anonymous_user = AnonymousUser