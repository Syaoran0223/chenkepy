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
    time_type = request.get('time_type')
    statistic_type = request.args.get('statistic_type')
    status = request.args.get('status')
    user = User.query.get_or_40(user_id)

    return {
        'sumary': [{
            'title': '录题',
            'done': 14,
            'doing': 2
        },
        {
            'title': '裁定',
            'done': 10,
            'doing': 2
        }],
        'statistic': [
            {'time': '2017-03-12', 'value': 12},
            {'time': '2017-03-13', 'value': 10},
        ]
    }