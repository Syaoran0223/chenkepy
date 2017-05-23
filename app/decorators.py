from functools import wraps
from flask import request, g, redirect, url_for
from flask.ext.login import current_user


def api_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated():
            return {
                'code': '403',
                'msg': '请登录后再访问'
            }
        return func(*args, **kwargs)
    return decorated_view

def admin_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not g.admin.is_authenticated():
            return {'msg': '请登录后再访问'}, 403
        return func(*args, **kwargs)
    return decorated_view

def admin_render_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not g.admin.is_authenticated():
            return redirect(url_for('admin.login'))
        return func(*args, **kwargs)
    return decorated_view

def super_admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not g.admin.is_super:
            return {'msg': '超级管理员才允许操作'}, 401
        return func(*args, **kwargs)
    return decorated_view

def permission_required(permission):
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated():
                return {
                    'code': '403',
                    'msg': '请登录后再访问'
                }
            if not permission in current_user.permissions:
                return {
                    'code': '401',
                    'msg': '权限不足'
                }
            return func(*args, **kwargs)
        return decorated_view
    return decorator
