#coding: utf-8

from flask import render_template, request, url_for, flash, redirect, session
from flask.ext.login import login_user,logout_user,login_required

from . import main
from .forms import LoginForm
from app.models import User, Region, School
from app.exceptions import JsonOutputException

@main.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        phone = request.form.get('phone')
        if not phone:
            raise JsonOutputException('请输入正确的手机号')
        session['phone'] = phone
        return {'code': 0}
    if session.get('phone'):
        return redirect(url_for('main.register_info'))
    return render_template('register.html')

@main.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
         user = User.query.filter_by(name=form.user_name.data).first()
         if user is None:
             user = User.query.filter_by(phone=form.user_name.data).first()
         if user is not None and user.verify_password(form.password.data):
             login_user(user)
             return redirect(request.args.get('next') or url_for('main.index'))
         flash('用户名或密码错误')
    return render_template('login.html',form=form)

@main.route('/register/info/')
def register_info():
    if not session.get('phone'):
        return redirect('main.register')
    provinces = Region.get_province()
    cities = Region.get_city(1257)
    areas = Region.get_area(1258)
    schools = School.get_schools_by_ctid(1260)
    return render_template('register_info.html',
        provinces=provinces,
        cities=cities,
        areas=areas,
        schools=schools)

@main.route('/')
def index():
    site_url = 'http://192.168.146.130:5000'
    return render_template('index.html', site_url=site_url)

@login_required
@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@amin.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
        flash('已发送密码重置的邮件至您注册时登记的邮箱中')
        return redirect(url_for('main.login'))
    return render_template('main/reset_password.html', form=form)


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
