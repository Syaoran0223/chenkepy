import json, math
from sqlalchemy import distinct
from app import db
from app.exceptions import JsonOutputException
from app.decorators import api_login_required, permission_required
from app.utils import upload, pagination
from flask import request, g
from app.const import QUEST_STATUS
from . import api_blueprint
from app.models import Question, QuestTyping, QOption, SubQuestion, Exam, School, QType
from app.utils import render_api
import datetime

#待录题列表
@api_blueprint.route('/paper/input/wait',methods=['GET'])
@api_login_required
@permission_required('INPUT_PERMISSION')
def input_wait():
    data = Question.get_exam_by_state(QUEST_STATUS['未处理'])
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
    selected_id = request.json.get('selected_id', 0)
    quest_content_html = request.json.get('quest_content_html')
    quest_content = request.json.get('quest_content')
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
    if selected_id:
        question.refer_quest_id = selected_id
        quest_typing_data.state = QUEST_STATUS['结束录题']
        question.state = QUEST_STATUS['结束录题']
        db.session.add(quest_typing_data)
        db.session.add(question)
        db.session.commit()

        # 检查试卷是否录题完毕
        exam = Exam.query.get(question.exam_id)
        exam.check_question_complete()
        return render_api({})
    if not quest_content_html:
        raise JsonOutputException('请输入题目')
    # 题目类型
    quest_type_id = request.json.get('quest_type_id')
    jieda = request.json.get('jieda', '')
    fenxi = request.json.get('fenxi', '')
    dianpin = request.json.get('dianpin', '')
    kaodian = request.json.get('kaodian', '')
    has_sub = request.json.get('has_sub', 0)
    quest_type = QType.query.filter_by(id=quest_type_id).first()
    if not quest_type:
        raise JsonOutputException('题型不存在')
    question.quest_content = quest_content
    question.quest_content_html = quest_content_html
    question.quest_type_id = quest_type_id
    question.jieda = jieda
    question.fenxi = fenxi
    question.dianpin = dianpin
    question.kaodian = kaodian
    question.has_sub = has_sub
    state = QUEST_STATUS['完成解答']
    # 大小题
    if has_sub:
        sub_items = request.json.get('sub_items1', [])
        for item in sub_items:
            item_quest_type_id = item.get('quest_type_id', 0)
            item_quest_type = QType.query.filter_by(id=item_quest_type_id).first()
            if not item_quest_type:
                raise JsonOutputException('子题题型不存在')
            correct_answer = item.get('correct_answer', '')
            if correct_answer == '':
                state = QUEST_STATUS['完成录题']
                break
            if item_quest_type.is_selector():
                options = item.get('options', [])
                option_count = len(options)
                if option_count == 0:
                    raise JsonOutputException('请输入选择题选项')
        question.sub_items1 = []
        for item in sub_items:
            item['operator_id'] = g.user.id
            item['finish_state'] = 'input'
            question.sub_items1.append(item)
    else:
        # 选择题
        if quest_type.is_selector():
            options1 = request.json.get('options1', [])
            option_count = len(options1)
            correct_answer1 = request.json.get('correct_answer1', '')
            show_type = request.json.get('show_type', 'C')
            if show_type == 'C':
                qcols = 1
                qrows = option_count / qcols
            if show_type == 'B':
                qrows = 2
                qcols = math.ceil(option_count / qrows)
            if show_type == 'A':
                qrows = 1
                qcols = option_count / qrows
            question.option_count = option_count
            question.qrows = qrows
            question.qcols = qcols
            question.correct_answer1 = correct_answer1
            if not question.correct_answer1:
                state = QUEST_STATUS['完成录题']
            # 插入选项
            question.options1 = options1
        # 解答/填空
        else:
            correct_answer1 = request.json.get('quest_answer', '')
            question.correct_answer1 = correct_answer1
            if question.correct_answer1 == '':
                state = QUEST_STATUS['完成录题']
    quest_typing_data.state = state
    question.state = state
    db.session.add(quest_typing_data)
    db.session.add(question)
    db.session.commit()
    return render_api({})
           
        

# 录题记录
@api_blueprint.route('/paper/input/list')
@api_login_required
@permission_required('INPUT_PERMISSION')
def input_list():
    res = Exam.get_deal_list(QuestTyping)
    return render_api(res)