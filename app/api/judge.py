import json, math
from app import db
from app.exceptions import JsonOutputException
from app.decorators import api_login_required, permission_required
from app.utils import upload, pagination
from flask import request, g
from app.const import QUEST_STATUS
from . import api_blueprint
from app.models import Question, QuestJudge, QOption, SubQuestion, Exam, QType
from app.utils import render_api
import datetime

#待检查列表
@api_blueprint.route('/quest/judge/wait',methods=['GET'])
@api_login_required
@permission_required('JUDGE_PERMISSION')
def judge_wait():
    data = Question.get_exam_by_state(QUEST_STATUS['待裁定'])
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
    res = Exam.get_deal_list(QuestJudge)
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
    # 大小题
    if question.has_sub:
        for item in getattr(question, sub_item_key):
            item_quest_type_id = item.get('quest_type_id', 0)
            item_quest_type = QType.query.filter_by(id=item_quest_type_id).first()
            if not item_quest_type:
                raise JsonOutputException('子题题型不存在')
            sub_quest = SubQuestion(parent_id=question.id,
                quest_content=item.get('quest_content', ''),
                quest_content_html=item.get('quest_content_html', ''),
                correct_answer=item.get('correct_answer', ''),
                quest_no=item.get('sort', 0),
                qtype_id=item_quest_type_id,
                operator_id=item.get('operator_id', 0),
                finish_state=item.get('finish_state', ''))
            if iitem_quest_type.is_selector():
                options = item.get('options', [])
                option_count = len(options)
                # 插入选项
                sub_quest.qoptjson = json.dumps(options)
                sub_quest.option_count = option_count
            db.session.add(sub_quest)
    else:
        # 选择题
        quest_type = QType.query.filter_by(id=question.quest_type_id).first()
        if not quest_type:
            raise JsonOutputException('题型不存在')
        if quest_type.is_selector():
            question.correct_answer = getattr(question, correct_answer_key)
            for option in getattr(question, option_key):
                option = QOption(
                    qid = question.id,
                    qok = option.get('_selected', False),
                    qsn = option.get('sort', ''),
                    qopt = option.get('content', '')
                )
                db.session.add(option)
        else:
            question.correct_answer = getattr(question, correct_answer_key)
    quest_judge_data.state = state
    question.state = state
    db.session.add(quest_judge_data)
    db.session.add(question)
    db.session.commit()
    return render_api({})