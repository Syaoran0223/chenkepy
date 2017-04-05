#coding: utf-8

from flask import request, g
from app.exceptions import AdminException
from app.decorators import admin_login_required
from app.search import Search
from app.models import Exam

from . import admin

@admin.route('/exams', methods=['GET'])
@admin_login_required
def get_exams():
    search = Search()
    res = search.load(Exam).paginate()
    return res