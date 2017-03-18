#coding: utf-8

import json
from flask import render_template, request, url_for, flash, redirect, session, g, current_app
from flask.ext.login import login_user,logout_user,login_required,current_user

from . import admin

from .forms import LoginForm
from app.models import Admin

@main.route('/login/', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
         admin = Admin.query.filter_by(name=form.user_name.data).first()
         if admin is None:
             admin = Admin.query.filter_by(phone=form.user_name.data).first()
         if admin is not None and admin.verify_password(form.password.data):
             login_user(admin)
             flash('登录成功')
             return redirect(request.args.get('next') or url_for('admin.index'))
         flash('用户名或密码错误')
    return render_template('admin_login.html', form=form)

@main.route('/')
@login_required
def index():
    site_url = current_app.config['SITE_URL']
    user_info = current_user.to_dict()
    user_info = json.dumps(user_info)
    menus = g.user.get_menus()
    menus = json.dumps(menus)
    return render_template('index.html',
        site_url=site_url, user_info=user_info, menus=menus)

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))