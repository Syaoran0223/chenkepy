#coding: utf-8

from flask import session, g
from app.models.users import AnonymousUser
from app.models import Admin


def get_admin():
    admin_id = session.get('admin_id')
    if not admin_id:
        return AnonymousUser()
    admin = Admin.query.get(admin_id)
    if not admin:
        admin = AnonymousUser()
        logout_admin()
    return admin

def login_admin(admin):
    if not admin.is_active():
        return False
    session['admin_id'] = admin.id
    g.admin = admin
    return True

def logout_admin():
    session.pop('admin_id')