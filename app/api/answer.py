import json, math
from app import db
from app.exceptions import JsonOutputException
from app.decorators import api_login_required, permission_required
from app.utils import upload, pagination
from flask import request, g
from app.const import QUEST_STATUS
from . import api_blueprint
from app.models import Question, QuestAnswer, QOption, SubQuestion
from app.utils import render_api
import datetime

#待录题列表
@api_blueprint.route('/paper/answer/wait',methods=['GET'])
@api_login_required
@permission_required('ANSWER_PERMISSION')
def answer_wait():
    data = Question.get_quest_by_state(QUEST_STATUS['完成录题'])
    return render_api(data)

# 领取录题任务
@api_blueprint.route('/paper/answer/<int:id>')
@api_login_required
@permission_required('ANSWER_PERMISSION')
def get_answer_task(id):
    question = Question.query.get(id)
    if not question:
        raise JsonOutputException('题目不存在')
    if question.state != QUEST_STATUS['完成录题'] and question.state != QUEST_STATUS['正在解答']:
        raise JsonOutputException('暂时无法处理该题目')
    quest_answer_data = QuestAnswer.query.\
        filter_by(state=QUEST_STATUS['正在解答']).\
        filter_by(quest_id=id).\
        order_by(QuestAnswer.created_at.desc()).\
        first()
    if not quest_answer_data:
        quest_answer_data = QuestAnswer(
            quest_id=id,
            exam_id=question.exam_id,
            quest_no=question.quest_no,
            state=QUEST_STATUS['正在解答'],
            operator_id=g.user.id,
        )
        quest_answer_data.save()
    if quest_answer_data.operator_id != g.user.id:
        raise JsonOutputException('该题目已被他人领取')
    question.state = QUEST_STATUS['正在解答']
    question.save()
    res = question.get_answer_dtl()
    return render_api(res)

# 答题记录
@api_blueprint.route('/paper/answer/list')
@api_login_required
@permission_required('ANSWER_PERMISSION')
def answer_list():
    query = QuestAnswer.query.\
        filter_by(operator_id=g.user.id)
    res = pagination(query, None, False)
    items = [item.get_question_dtl() for item in res['items']]
    res['items'] = items
    return render_api(res)

# 题目解答
@api_blueprint.route('/paper/answer/<int:id>', methods=['PUT'])
@api_login_required
@permission_required('ANSWER_PERMISSION')
def answer_quest(id):
    question = Question.query.get(id)
    if not question:
        raise JsonOutputException('题目不存在')
    if question.state != QUEST_STATUS['正在解答']:
        raise JsonOutputException('暂时无法处理该题目')
    quest_answer_data = QuestAnswer.query.\
        filter_by(state=QUEST_STATUS['正在解答']).\
        filter_by(quest_id=id).\
        order_by(QuestAnswer.created_at.desc()).\
        first()
    if quest_answer_data.operator_id != g.user.id:
        raise JsonOutputException('该题目已被他人领取')

    # 题目类型
    jieda = request.json.get('jieda', '')
    fenxi = request.json.get('fenxi', '')
    dianpin = request.json.get('dianpin', '')
    kaodian = request.json.get('kaodian', '')
    question.jieda = jieda
    question.fenxi = fenxi
    question.dianpin = dianpin
    question.kaodian = kaodian
    state = QUEST_STATUS['完成解答']
    quest_type_id = request.json.get('quest_type_id')
    # 大小题
    if question.has_sub:
        sub_items = request.json.get('sub_items1', [])
        if len(sub_items) == 0:
            raise JsonOutputException('请输入子题信息')
        for item in sub_items:
            item_quest_type_id = item.get('quest_type_id', 0)
            correct_answer = item.get('correct_answer', '')
            if correct_answer == '':
                raise JsonOutputException('子题({})请输入正确答案'.format(item.get('sort', '')))
            if item_quest_type_id == '1':
                options = item.get('options', [])
                option_count = len(options)
                if option_count == 0:
                    raise JsonOutputException('子题({})请输入正确答案'.format(item.get('sort', '')))
            elif item_quest_type_id == '2':
                correct_answer = item.get('correct_answer', [])
                if len(correct_answer) == 0:
                    raise JsonOutputException('子题({})请输入正确答案'.format(item.get('sort', '')))
            elif item_quest_type_id == '3':
                pass
            else:
                raise JsonOutputException('子题题型错误')
        question.sub_items1 = []
        for item in sub_items:
            item['operator_id'] = g.user.id
            item['finish_state'] = 'answer'
            question.sub_items1.append(item)
    else:
        # 选择题
        if quest_type_id == '1':
            options1 = request.json.get('options1', [])
            correct_answer1 = request.json.get('correct_answer1', '')
            if not correct_answer1:
                raise JsonOutputException('请输入正确答案')
            question.correct_answer1 = correct_answer1
            # 修改选项选中状态
            question.options1 = options1
        # 填空
        elif quest_type_id == '2':
            correct_answer1 = request.json.get('correct_answer1', [])
            answer_list1 = request.json.get('answer_list1', [])
            question.answer_list1 = answer_list1
            if len(correct_answer1) == 0:
                raise JsonOutputException('请输入正确答案')
            correct_answer1 = json.dumps(correct_answer1)
            question.correct_answer1 = correct_answer1
            
        # 解答
        elif quest_type_id == '3':
            correct_answer1 = request.json.get('quest_answer', '')
            question.correct_answer1 = correct_answer1
            if question.correct_answer1 == '':
                raise JsonOutputException('请输入正确答案')
        else:
            raise JsonOutputException('题型错误')
    quest_answer_data.state = state
    question.state = state
    db.session.add(quest_answer_data)
    db.session.add(question)
    db.session.commit()
    return render_api({})