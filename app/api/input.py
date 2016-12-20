import json, math
from app import db
from app.exceptions import JsonOutputException
from app.decorators import api_login_required, permission_required
from app.utils import upload, pagination
from flask import request, g
from app.const import QUEST_STATUS
from . import api_blueprint
from app.models import Question, QuestTyping, QOption
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

# 题目录入
@api_blueprint.route('/paper/input/<int:id>', methods=['PUT'])
@api_login_required
@permission_required('INPUT_PERMISSION')
def input_quest(id):
    quest_content_html = request.json.get('quest_content_html')
    quest_content = request.json.get('quest_content')
    if not quest_content_html:
        raise JsonOutputException('请输入题目')
    question = Question.query.get(id)
    if not question:
        raise JsonOutputException('题目不存在')
    if question.state != QUEST_STATUS['正在录题']:
        raise JsonOutputException('暂时无法处理该题目')
    quest_typing_data = QuestTyping.query.\
        filter_by(state=QUEST_STATUS['正在录题']).\
        filter_by(quest_id=id).\
        order_by(QuestTyping.created_at.desc()).\
        first()
    if quest_typing_data.operator_id != g.user.id:
        raise JsonOutputException('该题目已被他人领取')
    # 题目类型
    quest_type_id = request.json.get('quest_type_id')
    jieda = request.json.get('jieda', '')
    fenxi = request.json.get('fenxi', '')
    dianpin = request.json.get('dianpin', '')
    kaodian = request.json.get('kaodian', '')
    question.quest_content = quest_content
    question.quest_content_html = quest_content_html
    question.quest_type_id = quest_type_id
    question.jieda = jieda
    question.fenxi = fenxi
    question.dianpin = dianpin
    question.kaodian = kaodian
    question.has_sub = False
    # 选择题
    if quest_type_id == '1':
        options = request.json.get('options', [])
        option_count = len(options)
        correct_answer = request.json.get('correct_answer', '')
        show_type = request.json.get('show_type', 'C')
        if show_type == 'C':
            qcols = 1
            qrows = option_count / qcols
        if show_type == 'B':
            qrows = 2
            qcols = math.ceil(options / qrows)
        if show_type == 'A':
            qrows = 1
            qcols = option_count / qrows
        question.option_count = option_count
        question.qrows = qrows
        question.qcols = qcols
        question.correct_answer = correct_answer
        # 插入选项
        for option in options:
            option = QOption(
                qid = question.id,
                qok = option.get('_selected', False),
                qsn = option.get('sort', ''),
                qopt = option.get('content', '')
            )
            db.session.add(option)
    # 填空
    if quest_type_id == '2':
        correct_answer = request.json.get('correct_answer', [])
        correct_answer = json.dumps(correct_answer)
        question.correct_answer = correct_answer
        
    # 解答
    if quest_type_id == '3':
        correct_answer = request.json.get('quest_answer', '')
        question.correct_answer = correct_answer
    else:
        raise JsonOutputException('题型错误')
    quest_typing_data.state = QUEST_STATUS['完成入题']
    question.state = QUEST_STATUS['完成入题']
    db.session.add(quest_typing_data)
    db.session.add(question)
    db.session.commit()
    return render_api({})
           
        

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