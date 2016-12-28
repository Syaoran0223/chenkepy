import json, math
from app import db
from app.exceptions import JsonOutputException
from app.decorators import api_login_required, permission_required
from app.utils import upload, pagination
from flask import request, g
from app.const import QUEST_STATUS
from . import api_blueprint
from app.models import Question, QuestTyping, QOption, SubQuestion
from app.utils import render_api
import datetime

#待录题列表
@api_blueprint.route('/paper/answer/wait',methods=['GET'])
@api_login_required
@permission_required('ANSWER_PERMISSION')
def answer_wait():
    data = Question.get_quest_by_state(QUEST_STATUS['待解答'])
    return render_api(data)