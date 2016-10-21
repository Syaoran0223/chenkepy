#coding: utf-8

from flask import g
from flask.ext.login import current_user
from . import main

# 初始化g.user
@main.before_request
def before_request():
    g.user = current_user