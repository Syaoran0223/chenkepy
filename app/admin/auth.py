#coding: utf-8

import json
from flask import render_template, request, url_for, redirect, g
from app.exceptions import AdminException
from app.models import Admin
from .login_service import login_admin, logout_admin
from app.decorators import admin_login_required, admin_render_login_required
from . import admin as admin

@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if g.admin.is_authenticated():
            return redirect(url_for('admin.index'))
        return render_template('admin_login.html')
    phone = request.json.get('phone')
    password = request.json.get('password')
    if not phone or not password:
        raise AdminException('请输入手机号和密码')

    admin = Admin.query.filter_by(phone=phone).first()
    if admin is not None and admin.verify_password(password):
        login_admin(admin)
        return {}
    raise AdminException('手机号或密码错误')
    

@admin.route('/')
@admin_render_login_required
def index():
    return render_template('admin_index.html', admin=g.admin.name)

@admin.route("/logout")
@admin_render_login_required
def logout():
    logout_admin()
    return redirect(url_for('admin.login'))