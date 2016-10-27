#coding: utf-8

import json
from flask import render_template, request, url_for, flash, redirect, session, g
from flask.ext.login import login_user,logout_user,login_required,current_user

from . import main

from .forms import LoginForm, RegisterForm, PasswordResetRequestForm, PasswordResetForm, RegisterInfoForm
from app.models import User, Region, School, InviteCode

from app.sms import SmsServer
@main.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        phone = form.phone.data
        user = User.query.filter_by(phone=phone).first()
        if user is not None:
            flash('该手机号已经注册过')
            return render_template('register.html', form=form)
        sms = SmsServer()
        # 验证码验证
        if not sms.check_code(form.valid_code.data, phone):
            flash('验证码错误')
            return render_template('register.html', form=form)
        if not InviteCode.get_code(form.visit_code.data):
            flash('邀请码错误')
            return render_template('register.html', form=form)
        session['phone'] = phone
        return redirect(url_for('main.register_info'))
    else:
        flash(form.errors)
    return render_template('register.html', form=form)

@main.route('/login/', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
         user = User.query.filter_by(name=form.user_name.data).first()
         if user is None:
             user = User.query.filter_by(phone=form.user_name.data).first()
         if user is not None and user.verify_password(form.password.data):
             login_user(user)
             flash('登录成功')
             return redirect(request.args.get('next') or url_for('main.index'))
         flash('用户名或密码错误')
    return render_template('login.html', form=form)

@main.route('/register/info/', methods=['GET', 'POST'])
def register_info():
    if not session.get('phone'):
        return redirect('main.register')
    form = RegisterInfoForm()
    if form.validate_on_submit():
        user = User(name=form.user_name.data,
            phone=form.phone.data,
            email=form.email.data,
            password=form.password.data,
            school_id=form.school_id.data,
            city_id=form.city_id.data,
            grade_id=form.grade_id.data)
        user.save()
        login_user(user)
        flash('注册成功')
        return render_template('main.index')
        #return redirect(url_for('main.index'))
    return render_template('register_info.html', form=form)

@main.route('/')
@login_required
def index():
    site_url = 'http://127.0.0.1:5000'
    user_info = current_user.to_dict()
    user_info = json.dumps(user_info)
    return render_template('index.html', site_url=site_url, user_info=user_info)

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    pass
    # if not current_user.is_anonymous:
    #     return redirect(url_for('main.index'))
    # form = PasswordResetRequestForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(email=form.email.data).first()
    #     if user:
    #         token = user.generate_reset_token()
    #     flash('已发送密码重置的邮件至您注册时登记的邮箱中')
    #     return redirect(url_for('main.login'))
    # return render_template('main/reset_password.html', form=form)


@main.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@main.route('/todo')
def todo():
    res = {
        'code': 0,
        'data': [],
        'msg': None
    }
    return res
