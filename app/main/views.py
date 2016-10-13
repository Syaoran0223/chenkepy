from flask import render_template, request, url_for, flash, redirect, session
from flask.ext.login import login_user

from . import main
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
    # form = LoginFrom()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(email=form.email.data).first()
    #     if user is not None and user.verify_password(form.password.data):
    #         login_user(user)
    #         return redirect(request.args.get('next') or url_for('admin.get_blogs'))
    #     flash('password error')
    return render_template('login.html')

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
    site_url = 'http://127.0.0.1:5000'
    return render_template('index.html', site_url=site_url)

@main.route('/todo')
def todo():
    res = {
        'code': 0,
        'data': [],
        'msg': None
    }
    return res