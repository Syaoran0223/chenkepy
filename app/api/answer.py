import json, math
from app import db
from app.exceptions import JsonOutputException
from app.decorators import api_login_required, permission_required
from app.utils import upload, pagination
from flask import request, g
from app.const import QUEST_STATUS
from . import api_blueprint
from app.models import Question, QuestAnswer, QOption, SubQuestion, Exam, QType
from app.utils import render_api
import datetime

#待录题列表
@api_blueprint.route('/paper/answer/wait',methods=['GET'])
@api_login_required
@permission_required('ANSWER_PERMISSION')
def answer_wait():
    data = Question.get_exam_by_state(QUEST_STATUS['完成录题'])
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
    res = Exam.get_deal_list(QuestAnswer)
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
    quest_content_html = request.json.get('quest_content_html')
    quest_content = request.json.get('quest_content')
    question.jieda = jieda
    question.fenxi = fenxi
    question.dianpin = dianpin
    question.kaodian = kaodian
    question.quest_content_html = quest_content_html
    question.quest_content = quest_content
    state = QUEST_STATUS['完成解答']
    quest_type_id = request.json.get('quest_type_id')
    quest_type = QType.query.filter_by(id=quest_type_id).first()
    if not quest_type:
        raise JsonOutputException('题型不存在')
    # 大小题
    if question.has_sub:
        sub_items = request.json.get('sub_items1', [])
        if len(sub_items) == 0:
            raise JsonOutputException('请输入子题信息')
        for item in sub_items:
            item_quest_type_id = item.get('quest_type_id', 0)
            item_quest_type = QType.query.filter_by(id=item_quest_type_id).first()
            if not item_quest_type:
                raise JsonOutputException('子题题型不存在')
            correct_answer = item.get('correct_answer', '')
            if correct_answer == '':
                raise JsonOutputException('子题({})请输入正确答案'.format(item.get('sort', '')))
            if item_quest_type.is_selector():
                options = item.get('options', [])
                option_count = len(options)
                if option_count == 0:
                    raise JsonOutputException('子题({})请输入正确答案'.format(item.get('sort', '')))
        question.sub_items1 = []
        for item in sub_items:
            item['operator_id'] = g.user.id
            item['finish_state'] = 'answer'
            question.sub_items1.append(item)
    else:
        # 选择题
        if quest_type.is_selector():
            options1 = request.json.get('options1', [])
            correct_answer1 = request.json.get('correct_answer1', '')
            if not correct_answer1:
                raise JsonOutputException('请输入正确答案')
            question.correct_answer1 = correct_answer1
            # 修改选项选中状态
            question.options1 = options1
        # 解答/填空
        else:
            correct_answer1 = request.json.get('quest_answer', '')
            question.correct_answer1 = correct_answer1
            if question.correct_answer1 == '':
                raise JsonOutputException('请输入正确答案')
    quest_answer_data.state = state
    question.state = state
    db.session.add(quest_answer_data)
    db.session.add(question)
    db.session.commit()
    return render_api({})