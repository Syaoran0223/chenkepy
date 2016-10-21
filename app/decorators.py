from functools import wraps
from flask import request
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