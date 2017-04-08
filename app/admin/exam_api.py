#coding: utf-8

from flask import request, g
from app.exceptions import AdminException
from app.decorators import admin_login_required
from app.search import Search
from app.models import Exam
from app.utils import pagination

from . import admin

@admin.route('/exams', methods=['GET'])
@admin_login_required
def get_exams():
    search = Search()
    res = search.load(Exam).paginate()
    return res

@admin.route('/exams/statistic', methods=['GET'])
@admin_login_required
def exam_statistic():
    sumary = Exam.get_sumary(request.args)
    time_line = Exam.get_timeline(request.args)
    statistic = Exam.get_statistic(request.args)
    return {
        'sumary': sumary,
        'time_line': time_line,
        'statistic': statistic
    }

@admin.route('/exams/suggest', methods=['GET'])
@admin_login_required
def get_exam_suggest():
    res = Exam.get_suggest(request.args)
    return res