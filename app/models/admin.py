from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db
from flask_login import UserMixin
from app import db
from ._base import SessionMixin

class Admin(db.Model, SessionMixin, UserMixin):
    __tablename__ = 'admin'
    protected_field = ['password','password_hash', 'last_login_ip']
    search_fields = ['name_like', 'phone_like', 'state', 'created_at_begin', 'created_at_end']

    def __init__(self, *args, **kwargs):
        Admin.register()
        super(Admin, self).__init__(*args, **kwargs)

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

    def __repr__(self):
        return '<Admin: %r>' % self.name