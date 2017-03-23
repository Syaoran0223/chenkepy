#coding: utf-8

from flask import g, session
from flask.ext.login import current_user
from app.admin.login_service import get_admin
from . import main

# 初始化g.user
@main.before_app_request
def before_request():
    g.user = current_user
    g.admin = get_admin()