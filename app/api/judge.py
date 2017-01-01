import json, math
from app import db
from app.exceptions import JsonOutputException
from app.decorators import api_login_required, permission_required
from app.utils import upload, pagination
from flask import request, g
from app.const import QUEST_STATUS
from . import api_blueprint
from app.models import Question, QuestJudge, QOption, SubQuestion
from app.utils import render_api
import datetime

#待检查列表
@api_blueprint.route('/quest/judge/wait',methods=['GET'])
@api_login_required
@permission_required('JUDGE_PERMISSION')
def judge_wait():
    data = Question.get_quest_by_state(QUEST_STATUS['待裁定'])
    return render_api(data)

# 领取裁定任务
@api_blueprint.route('/quest/judge/<int:id>')
@api_login_required
@permission_required('JUDGE_PERMISSION')
def get_judge_task(id):
    question = Question.query.get(id)
    if not question:
        raise JsonOutputException('题目不存在')
    if question.state != QUEST_STATUS['待裁定'] and question.state != QUEST_STATUS['正在裁定']:
        raise JsonOutputException('暂时无法处理该题目')
    quest_judge_data = QuestJudge.query.\
        filter_by(state=QUEST_STATUS['正在裁定']).\
        filter_by(quest_id=id).\
        order_by(QuestJudge.created_at.desc()).\
        first()
    if not quest_judge_data:
        quest_judge_data = QuestJudge(
            quest_id=id,
            exam_id=question.exam_id,
            quest_no=question.quest_no,
            state=QUEST_STATUS['正在裁定'],
            operator_id=g.user.id,
        )
        quest_judge_data.save()
    if quest_judge_data.operator_id != g.user.id:
        raise JsonOutputException('该题目已被他人领取')
    question.state = QUEST_STATUS['正在裁定']
    question.save()
    res = question.get_answer_dtl()
    return render_api(res)

# 裁定记录
@api_blueprint.route('/quest/judge/list')
@api_login_required
@permission_required('JUDGE_PERMISSION')
def judge_list():
    query = QuestJudge.query.\
        filter_by(operator_id=g.user.id)
    res = pagination(query, None, False)
    items = [item.get_question_dtl() for item in res['items']]
    res['items'] = items
    return render_api(res)

# 裁定结果
@api_blueprint.route('/quest/judge/accept/<int:id>', methods=['POST'])
@api_login_required
@permission_required('JUDGE_PERMISSION')
def judge_accepy(id):
    types = request.json.get('type')
    if not types in [1,2]:
        raise JsonOutputException('请求参数错误')
    question = Question.query.get(id)
    if not question:
        raise JsonOutputException('题目不存在')
    if question.state != QUEST_STATUS['正在裁定']:
        raise JsonOutputException('暂时无法处理该题目')
    quest_judge_data = QuestJudge.query.\
        filter_by(state=QUEST_STATUS['正在裁定']).\
        filter_by(quest_id=id).\
        order_by(QuestJudge.created_at.desc()).\
        first()
    if quest_judge_data.operator_id != g.user.id:
        raise JsonOutputException('该题目已被他人领取')
    state = QUEST_STATUS['待校对']
    correct_answer_key = 'correct_answer{}'.format(types)
    option_key = 'options{}'.format(types)
    sub_item_key = 'sub_items{}'.format(types)
    # 选择题
    if question.quest_type_id == '1':
        question.correct_answer = getattr(question, correct_answer_key)
        for option in getattr(question, option_key):
            option = QOption(
                qid = question.id,
                qok = option.get('_selected', False),
                qsn = option.get('sort', ''),
                qopt = option.get('content', '')
            )
            db.session.add(option)
    elif question.quest_type_id == '2' or question.quest_type_id == '3':
        question.correct_answer = getattr(question, correct_answer_key)
    elif question.quest_type_id == '4':
        for item in getattr(question, sub_item_key):
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
    quest_judge_data.state = state
    question.state = state
    db.session.add(quest_judge_data)
    db.session.add(question)
    db.session.commit()
    return render_api({})