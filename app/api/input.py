import json
from app.exceptions import JsonOutputException
from app.decorators import api_login_required, permission_required
from app.utils import upload, pagination
from flask import request, g
from app.const import QUEST_STATUS
from . import api_blueprint
from app.models import Question, QuestTyping
from app.utils import render_api
import datetime

#待录题列表
@api_blueprint.route('/paper/input/wait',methods=['GET'])
@api_login_required
@permission_required('INPUT_PERMISSION')
def input_wait():
    data = Question.get_quest_by_state(QUEST_STATUS['未处理'])
    return render_api(data)

# 领取录题任务
@api_blueprint.route('/paper/input/<int:id>')
@api_login_required
@permission_required('INPUT_PERMISSION')
def get_input_task(id):
    question = Question.query.get(id)
    if not question:
        raise JsonOutputException('题目不存在')
    if question.state != QUEST_STATUS['未处理'] and question.state != QUEST_STATUS['正在录题']:
        raise JsonOutputException('暂时无法处理该题目')
    quest_typing_data = QuestTyping.query.\
        filter_by(state=QUEST_STATUS['正在录题']).\
        filter_by(quest_id=id).\
        order_by(QuestTyping.created_at.desc()).\
        first()
    if not quest_typing_data:
        quest_typing_data = QuestTyping(
            quest_id=id,
            exam_id=question.exam_id,
            quest_no=question.quest_no,
            state=QUEST_STATUS['正在录题'],
            operator_id=g.user.id,
        )
        quest_typing_data.save()
    if quest_typing_data.operator_id != g.user.id:
        raise JsonOutputException('该题目已被他人领取')
    question.state = QUEST_STATUS['正在录题']
    question.save()
    res = question.get_dtl()
    return render_api(res)

# 录题记录
@api_blueprint.route('/paper/input/list')
@api_login_required
@permission_required('INPUT_PERMISSION')
def input_list():
    query = QuestTyping.query.\
        filter_by(operator_id=g.user.id)
    res = pagination(query, None, False)
    items = [item.get_question_dtl() for item in res['items']]
    res['items'] = items
    return render_api(res)