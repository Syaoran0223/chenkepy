#coding: utf-8

from flask import request, g
from app.exceptions import AdminException
from app.decorators import admin_login_required
from app.models import Question

from . import admin

@admin.route('/questions', methods=['GET'])
@admin_login_required
def get_questions():
    res = Question.search(request.args)
    return res

@admin.route('/questions/statistic', methods=['GET'])
@admin_login_required
def question_statistics():
    sumary = Question.get_sumary(request.args)
    time_line = Question.get_timeline(request.args)
    statistic = Question.get_statistic(request.args)
    return {
        'sumary': sumary,
        'time_line': time_line,
        'statistic': statistic
    }