from . import main
from flask import render_template

@main.route('/login')
def index():
    return render_template('login.html')

@main.route('/register')
def register():
    return render_template('register.html')

@main.route('/register/info')
def register_info():
    return render_template('register_info.html')