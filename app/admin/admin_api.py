#coding: utf-8

from flask import request, g
from app.exceptions import AdminException
from app.models import Admin
from app.decorators import admin_login_required
from app.search import Search

from . import admin

@admin.route('/admin', methods=['POST'])
@admin_login_required
def create():
    name = request.json.get('name')
    phone = request.json.get('phone')
    password = request.json.get('password')
    if not name:
        raise AdminException('请输入用户名')
    if not phone or not password:
        raise AdminException('请输入手机号和密码')
    admin = Admin.query.filter_by(phone=phone).first()
    if admin:
        raise AdminException('手机号已存在')
    admin = Admin(name=name, password=password, phone=phone)
    admin.save()
    return admin.to_dict()

@admin.route('/admin', methods=['GET'])
@admin_login_required
def get_admins():
    search = Search()
    res = search.load(Admin).paginate()
    return res

@admin.route('/admin/<int:id>')
@admin_login_required
def get_admin(id):
    admin = Admin.query.get_or_404(id)
    return admin.to_dict()

@admin.route('/admin/<int:id>', methods=['DELETE'])
@admin_login_required
def delete_admin(id):
    admin = Admin.query.get_or_404(id)
    if admin.id == g.admin.id:
        raise AdminException('不允许删除自己')
    admin.delete()
    return {}
