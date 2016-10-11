from . import main
from flask import render_template
from flask import jsonify

@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/register')
def register():
    return render_template('register.html')

@main.route('/register/info')
def register_info():
    return render_template('register_info.html')

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
    return jsonify(res)