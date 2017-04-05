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