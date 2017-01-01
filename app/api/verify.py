import json, math
from app import db
from app.exceptions import JsonOutputException
from app.decorators import api_login_required, permission_required
from app.utils import upload, pagination
from flask import request, g
from app.const import QUEST_STATUS
from . import api_blueprint
from app.models import Question, QuestVerify, QOption, SubQuestion
from app.utils import render_api
import datetime

#待校对列表
@api_blueprint.route('/quest/verify/wait',methods=['GET'])
@api_login_required
@permission_required('VERIFY_PERMISSION')
def verify_wait():
    data = Question.get_quest_by_state(QUEST_STATUS['待校对'])
    return render_api(data)

#领取校对任务
@api_blueprint.route('/quest/verify/<int:id>')
@api_login_required
@permission_required('VERIFY_PERMISSION')
def get_verify_task(id):
    question = Question.query.get(id)
    if not question:
        raise JsonOutputException('题目不存在')
    if question.state != QUEST_STATUS['待校对'] and question.state != QUEST_STATUS['正在校对']:
        raise JsonOutputException('暂时无法处理该题目')
    quest_verify_data = QuestVerify.query.\
        filter_by(state=QUEST_STATUS['正在校对']).\
        filter_by(quest_id=id).\
        order_by(QuestVerify.created_at.desc()).\
        first()
    if not quest_verify_data:
        quest_verify_data = QuestVerify(
            quest_id=id,
            exam_id=question.exam_id,
            quest_no=question.quest_no,
            state=QUEST_STATUS['正在校对'],
            operator_id=g.user.id,
        )
        quest_verify_data.save()
    if quest_verify_data.operator_id != g.user.id:
        raise JsonOutputException('该题目已被他人领取')
    question.state = QUEST_STATUS['正在校对']
    question.save()
    res = question.get_verify_dtl()
    return render_api(res)

# 校对记录
@api_blueprint.route('/quest/verify/list')
@api_login_required
@permission_required('VERIFY_PERMISSION')
def verify_list():
    query = QuestVerify.query.\
        filter_by(operator_id=g.user.id)
    res = pagination(query, None, False)
    items = [item.get_question_dtl() for item in res['items']]
    res['items'] = items
    return render_api(res)

# 校对正确
@api_blueprint.route('/quest/verify/right/<int:id>', methods=['PUT'])
@api_login_required
@permission_required('VERIFY_PERMISSION')
def verify_right(id):
    question = Question.query.get(id)
    if not question:
        raise JsonOutputException('题目不存在')
    if question.state != QUEST_STATUS['正在校对']:
        raise JsonOutputException('暂时无法处理该题目')
    quest_verify_data = QuestVerify.query.\
        filter_by(state=QUEST_STATUS['正在校对']).\
        filter_by(quest_id=id).\
        order_by(QuestVerify.created_at.desc()).\
        first()
    if quest_verify_data.operator_id != g.user.id:
        raise JsonOutputException('该题目已被他人领取')
    state = QUEST_STATUS['结束录题']
   
    quest_verify_data.state = state
    question.state = state
    db.session.add(quest_verify_data)
    db.session.add(question)
    db.session.commit()
    return render_api({})

# 重新输入答案
@api_blueprint.route('/quest/verify/<int:id>', methods=['PUT'])
@api_login_required
@permission_required('VERIFY_PERMISSION')
def verify_quest(id):
    question = Question.query.get(id)
    if not question:
        raise JsonOutputException('题目不存在')
    if question.state != QUEST_STATUS['正在校对']:
        raise JsonOutputException('暂时无法处理该题目')
    quest_verify_data = QuestVerify.query.\
        filter_by(state=QUEST_STATUS['正在校对']).\
        filter_by(quest_id=id).\
        order_by(QuestVerify.created_at.desc()).\
        first()
    if quest_verify_data.operator_id != g.user.id:
        raise JsonOutputException('该题目已被他人领取')

    # 题目类型
    jieda = request.json.get('jieda', '')
    fenxi = request.json.get('fenxi', '')
    dianpin = request.json.get('dianpin', '')
    kaodian = request.json.get('kaodian', '')
    quest_content = request.json.get('quest_content', '')
    quest_content_html = request.json.get('quest_content_html', '')
    question.jieda = jieda
    question.fenxi = fenxi
    question.dianpin = dianpin
    question.kaodian = kaodian
    question.quest_content = quest_content
    question.quest_content_html = quest_content_html
    state = QUEST_STATUS['结束录题']
    quest_type_id = request.json.get('quest_type_id')
    # 选择
    if quest_type_id == '1':
        options = request.json.get('options', [])
        for data in options:
            option = QOption.query.get(data['id'])
            if not option:
                continue
            option.qopt = data['content']
            db.session.add(option)
    # 大小题
    elif quest_type_id == '4':
        sub_items = request.json.get('sub_items', [])
        for item in sub_items:
            sub_item = SubQuestion.query.get(item.get('id', 0))
            if not sub_item:
                continue
            sub_quest_content = item.get('quest_content', '')
            sub_quest_content_html = item.get('quest_content_html', '')
            sub_item.quest_content = sub_quest_content
            sub_item.quest_content_html = sub_quest_content_html
            
            if sub_item.qtype_id == 1:
                options = item.get('options', [])
                sub_item.qoptjson = json.dumps(options)
            db.session.add(sub_item)
            
    quest_verify_data.state = state
    question.state = state
    db.session.add(quest_verify_data)
    db.session.add(question)
    db.session.commit()
    return render_api({})