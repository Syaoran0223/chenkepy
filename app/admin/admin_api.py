#coding: utf-8

from flask import request, g
from app.exceptions import AdminException
from app.models import Admin
from app.decorators import admin_login_required, super_admin_required
from app.search import Search

from . import admin

@admin.route('/admins', methods=['POST'])
@admin_login_required
@super_admin_required
def create():
    name = request.json.get('name')
    phone = request.json.get('phone')
    email = request.json.get('email')
    password = request.json.get('password')
    is_super = request.json.get('is_super') or False
    if not name:
        raise AdminException('请输入用户名')
    if not phone or not password:
        raise AdminException('请输入手机号和密码')
    admin = Admin.query.filter_by(phone=phone).first()
    if admin:
        raise AdminException('手机号已存在')
    admin = Admin(name=name, password=password, phone=phone, is_super=is_super, email=email)
    admin.save()
    return admin.to_dict()

@admin.route('/admins', methods=['GET'])
@admin_login_required
@super_admin_required
def get_admins():
    search = Search()
    res = search.load(Admin).paginate()
    return res

@admin.route('/admins/<int:id>')
@admin_login_required
@super_admin_required
def get_admin(id):
    admin = Admin.query.get_or_404(id)
    return admin.to_dict()

@admin.route('/admins/<int:id>', methods=['DELETE'])
@admin_login_required
@super_admin_required
def delete_admin(id):
    admin = Admin.query.get_or_404(id)
    if admin.id == g.admin.id:
        raise AdminException('不允许删除自己')
    admin.delete()
    return {}

@admin.route('/admins/<int:id>', methods=['PUT'])
@admin_login_required
@super_admin_required
def update_admin(id):
    admin = Admin.query.get_or_404(id)
    name = request.json.get('name')
    email = request.json.get('email')
    state = request.json.get('state')
    is_super = request.json.get('is_super')
    if admin:
        admin.name = name
    if email:
        admin.email = email
    if state:
        admin.state = state
    if is_super:
        admin.is_super = is_super
    admin.save()
    return admin.to_dict()
