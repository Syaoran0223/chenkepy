#coding: utf-8

from flask import request, g
from app.exceptions import AdminException
from app.models import User
from app.decorators import admin_login_required
from app.search import Search
from app.models.permissions import Permission

from . import admin

@admin.route('/users', methods=['GET'])
@admin_login_required
def get_users():
    search = Search()
    res = search.load(User).paginate()
    return res

@admin.route('/users/<int:id>')
@admin_login_required
def get_user(id):
    user = User.query.get_or_404(id)
    return user.to_dict()

@admin.route('/users/<int:id>', methods=['PUT'])
@admin_login_required
def update_user(id):
    user = User.query.get_or_404(id)
    permissions = request.json.get('permissions', [])
    for permission in permissions:
        if permission not in Permission.__dict__:
            raise AdminException('角色不合法')
    if not permissions:
        raise AdminException('请选择角色')
    user.permissions = permissions
    user.save()
    return user.to_dict()

    
@admin.route('/users/statistic')
@admin_login_required
def user_statistic():
    user_id = request.args.get('user_id')
    begin_time = request.args.get('begin_time')
    end_time = request.args.get('end_time')
    time_type = request.args.get('time_type')
    statistic_type = request.args.get('statistic_type', 'UPLOAD_PERMISSION')
    status = request.args.get('status')
    user = User.query.get_or_404(user_id)
    sumary = user.get_admin_summary(begin_time, end_time)
    statistic = user.get_statistic(begin_time, end_time, time_type, statistic_type, status)
    return {
        'sumary':sumary,
        'statistic': statistic
    }

@admin.route('/works')
@admin_login_required
def user_works():
    search = Search()
    res = search.load(User).paginate(to_dict=False)
    items = []
    for item in res['items']:
        sumary = item.get_admin_summary(False, False)
        item = item.to_dict()
        item['sumary'] = sumary
        items.append(item)
    res['items'] = items
    return res