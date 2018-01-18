#coding: utf-8

import json
import http.client, urllib.parse
import requests
from flask import render_template, request, url_for, flash, redirect, session, g, current_app
from flask.ext.login import login_user,logout_user,login_required,current_user

from . import main

from .forms import LoginForm, RegisterForm, PasswordResetRequestForm, PasswordResetForm, RegisterInfoForm
from app.models import User, Region, School, InviteCode, QType
from app.utils import render_api
from app.sms import SmsServer
from app.exceptions import JsonOutputException

def get_subjects_json():
    connection = http.client.HTTPConnection('i3ke.com', 80, timeout=10)
    headers = {'Content-type': 'application/json'}
    params = "{}"
    connection.request('GET', '/api/v2/subjects', params, headers)

    response = connection.getresponse()
    jsonStr = response.read().decode()
    subject_res = json.loads(jsonStr)
    subjects = []
    if subject_res.get('ok'):
        subjects = subject_res['data']['subjects']
    return subjects

def get_subjects():
    subjects = get_subjects_json()
    subjects = json.dumps(subjects)
    return subjects

@main.route('/api/subjects', methods=['GET'])
def get_subjects_api():
    data = get_subjects_json()
    return render_api(data)

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
        try:
            int(form.visit_code.data)
        except:
            flash('邀请码错误')
            return render_template('register.html', form=form)
        if not (len(form.visit_code.data)==4 and sum([int(i) for i in form.visit_code.data])==16):
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
        user = User.query.filter_by(phone=form.phone.data).first()
        if user is not None:
            flash('该手机号已经注册过')
            return render_template('register.html', form=form)
        user = User.query.filter_by(name=form.user_name.data).first()
        if user is not None:
            flash('该用户名已被使用')
            return render_template('register.html', form=form)
        user = User(name=form.user_name.data,
            phone=form.phone.data,
            email=form.email.data,
            password=form.password.data,
            school_id=form.school_id.data,
            city_id=form.city_id.data,
            grade_id=form.grade_id.data,
            province_id=form.province_id.data,
            area_id=form.area_id.data)
        user.save()
        login_user(user)
        flash('注册成功')
        return redirect(url_for('main.index'))
    return render_template('register_info.html', form=form)

@main.route('/')
@login_required
def index():
    site_url = current_app.config['SITE_URL']
    user_info = current_user.to_dict()
    user_info = json.dumps(user_info)
    menus = g.user.get_menus()
    menus = json.dumps(menus)
    
    subjects = get_subjects()
    qtypes = QType.query.all()
    qtypes = [{'id': t.id, 'subject_id': t.subject_id, 'text': t.name} for t in qtypes]
    qtypes = json.dumps(qtypes)

    return render_template('index.html',
        site_url=site_url, user_info=user_info,
        menus=menus, subjects=subjects, qtypes=qtypes)

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

@main.route('/wechat/login')
def wechat_login():
    return render_template('wechat/login.html')
	
@main.route('/wechat/register')
def wechat_register():
    return render_template('wechat/register.html')
	
@main.route('/wechat/fillInInfor')
def wechat_fillInInfor():
    subjects = get_subjects()
    return render_template('wechat/fill_in_infor.html', subjects=subjects)	

@main.route('/wechat/index')
def wechat_index():
    subjects = get_subjects()

    return render_template('wechat/index.html', subjects=subjects)

@main.route('/wechat/upload')
def wechat_upload():
    subjects = get_subjects()

    return render_template('wechat/upload_record.html', subjects=subjects)

@main.route('/wechat/user/<string:code>')
def get_user_by_openid(code):
    # 获取openid
    url = "https://api.weixin.qq.com/sns/jscode2session"
    querystring = {
        "appid": current_app.config['WECHAT_APPID'],
        "secret": current_app.config['WECHAT_SECRET'],
        "js_code": code,
        "grant_type": "authorization_code"
    }
    response = requests.request("GET", url, params=querystring)
    if not response.ok:
        raise JsonOutputException('openid获取失败')
    res = response.json()
    if res.get('errcode'):
        raise JsonOutputException(res['errmsg'])
    openid = res['openid']

    user = User.query.filter_by(openid=openid).first()
    session['openid'] = openid
    if not user:
        user = User(openid=openid)
        user.save()
        return render_api({
            'status': 'unregister'
        })
    if not user.phone:
        return render_api({
            'status': 'unregister'
        })
    login_user(user)
    data = user.to_dict()
    return render_api({
        'status': 'success',
        'user': data
    })