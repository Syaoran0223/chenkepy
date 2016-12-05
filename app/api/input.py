import json
from app.exceptions import JsonOutputException
from app.decorators import api_login_required, permission_required
from app.utils import upload, pagination
from flask import request, g
from app.const import QUEST_STATUS
from . import api_blueprint
from app.models import Question
from app.utils import render_api
import datetime

#待录题列表
@api_blueprint.route('/paper/input/wait',methods=['GET'])
@api_login_required
@permission_required('INPUT_PERMISSION')
def input_wait():
    data = Question.get_quest_by_state(QUEST_STATUS['未处理'])
    return render_api(data)
