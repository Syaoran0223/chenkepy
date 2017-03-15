import json, math
from app import db
from app.exceptions import JsonOutputException
from app.decorators import api_login_required, permission_required
from app.utils import upload, pagination
from flask import request, g
from app.const import QUEST_STATUS
from . import api_blueprint
from app.models import Question, QuestCheck, QOption, SubQuestion, Exam
from app.utils import render_api
import datetime

#待检查列表
@api_blueprint.route('/paper/answer/check/wait',methods=['GET'])
@api_login_required
@permission_required('CHECK_PERMISSION')
def answer_check_wait():
    data = Question.get_exam_by_state(QUEST_STATUS['完成解答'])
    return render_api(data)

# 领取检查任务
@api_blueprint.route('/paper/answer/check/<int:id>')
@api_login_required
@permission_required('CHECK_PERMISSION')
def get_check_task(id):
    question = Question.query.get(id)
    if not question:
        raise JsonOutputException('题目不存在')
    if question.state != QUEST_STATUS['完成解答'] and question.state != QUEST_STATUS['正在检查']:
        raise JsonOutputException('暂时无法处理该题目')
    quest_check_data = QuestCheck.query.\
        filter_by(state=QUEST_STATUS['正在检查']).\
        filter_by(quest_id=id).\
        order_by(QuestCheck.created_at.desc()).\
        first()
    if not quest_check_data:
        quest_check_data = QuestCheck(
            quest_id=id,
            exam_id=question.exam_id,
            quest_no=question.quest_no,
            state=QUEST_STATUS['正在检查'],
            operator_id=g.user.id,
        )
        quest_check_data.save()
    if quest_check_data.operator_id != g.user.id:
        raise JsonOutputException('该题目已被他人领取')
    question.state = QUEST_STATUS['正在检查']
    question.save()
    res = question.get_answer_dtl()
    return render_api(res)

# 检查记录
@api_blueprint.route('/paper/answer/check/list')
@api_login_required
@permission_required('CHECK_PERMISSION')
def check_list():
    res = Exam.get_deal_list(QuestCheck)
    return render_api(res)

# 答案正确
@api_blueprint.route('/paper/answer/check/right/<int:id>', methods=['PUT'])
@api_login_required
@permission_required('CHECK_PERMISSION')
def check_right(id):
    question = Question.query.get(id)
    if not question:
        raise JsonOutputException('题目不存在')
    if question.state != QUEST_STATUS['正在检查']:
        raise JsonOutputException('暂时无法处理该题目')
    quest_check_data = QuestCheck.query.\
        filter_by(state=QUEST_STATUS['正在检查']).\
        filter_by(quest_id=id).\
        order_by(QuestCheck.created_at.desc()).\
        first()
    if quest_check_data.operator_id != g.user.id:
        raise JsonOutputException('该题目已被他人领取')
    state = QUEST_STATUS['待校对']
    # 大小题
    if question.has_sub:
        for item in question.sub_items1:
            sub_quest = SubQuestion(parent_id=question.id,
                quest_content=item.get('quest_content', ''),
                quest_content_html=item.get('quest_content_html', ''),
                correct_answer=item.get('correct_answer', ''),
                quest_no=item.get('sort', 0),
                qtype_id=item.get('quest_type_id', 0),
                operator_id=item.get('operator_id', 0),
                finish_state=item.get('finish_state', ''))
            if int(sub_quest.qtype_id) == 1:
                options = item.get('options', [])
                option_count = len(options)
                # 插入选项
                sub_quest.qoptjson = json.dumps(options)
                sub_quest.option_count = option_count
            elif int(sub_quest.qtype_id) == 2:
                correct_answer = item.get('correct_answer', [])
                correct_answer = json.dumps(correct_answer)
                sub_quest.correct_answer = correct_answer
            elif int(sub_quest.qtype_id) == 3:
                pass
            db.session.add(sub_quest)
    else:
        # 选择题
        if question.quest_type_id == '1':
            question.correct_answer = question.correct_answer1
            for option in question.options1:
                option = QOption(
                    qid = question.id,
                    qok = option.get('_selected', False),
                    qsn = option.get('sort', ''),
                    qopt = option.get('content', '')
                )
                db.session.add(option)
        elif question.quest_type_id == '2' or question.quest_type_id == '3':
            question.correct_answer = question.correct_answer1  
    quest_check_data.state = state
    question.state = state
    db.session.add(quest_check_data)
    db.session.add(question)
    db.session.commit()
    return render_api({})

# 重新输入答案
@api_blueprint.route('/paper/answer/check/<int:id>', methods=['PUT'])
@api_login_required
@permission_required('CHECK_PERMISSION')
def check_quest(id):
    question = Question.query.get(id)
    if not question:
        raise JsonOutputException('题目不存在')
    if question.state != QUEST_STATUS['正在检查']:
        raise JsonOutputException('暂时无法处理该题目')
    quest_check_data = QuestCheck.query.\
        filter_by(state=QUEST_STATUS['正在检查']).\
        filter_by(quest_id=id).\
        order_by(QuestCheck.created_at.desc()).\
        first()
    if quest_check_data.operator_id != g.user.id:
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
    state = QUEST_STATUS['待裁定']
    quest_type_id = request.json.get('quest_type_id')
    # 大小题
    if question.has_sub:
        sub_items = request.json.get('sub_items2', [])
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
        question.sub_items2 = []
        for item in sub_items:
            item['operator_id'] = g.user.id
            item['finish_state'] = 'answer_check'
            question.sub_items2.append(item)
    else:
        # 选择
        if quest_type_id == '1':
            correct_answer2 = request.json.get('correct_answer2', '')
            if not correct_answer2:
                raise JsonOutputException('请输入正确答案')
            options2 = request.json.get('options2', [])
            question.correct_answer2 = correct_answer2
            question.options2 = options2
        # 填空
        elif quest_type_id == '2':
            correct_answer2 = request.json.get('correct_answer2', [])
            answer_list2 = request.json.get('answer_list2', [])
            if len(correct_answer2) == 0:
                raise JsonOutputException('请输入正确答案')
            correct_answer2 = json.dumps(correct_answer2)
            question.correct_answer2 = correct_answer2
            question.answer_list2 = answer_list2
            
        # 解答
        elif quest_type_id == '3':
            correct_answer2 = request.json.get('correct_answer2', '')
            question.correct_answer2 = correct_answer2
            if not question.correct_answer2:
                raise JsonOutputException('请输入正确答案')
        else:
            raise JsonOutputException('题型错误')
    quest_check_data.state = state
    question.state = state
    db.session.add(quest_check_data)
    db.session.add(question)
    db.session.commit()
    return render_api({})