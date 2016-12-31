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

# # 答案正确
# @api_blueprint.route('/paper/answer/check/right/<int:id>', methods=['PUT'])
# @api_login_required
# @permission_required('JUDGE_PERMISSION')
# def check_right(id):
#     question = Question.query.get(id)
#     if not question:
#         raise JsonOutputException('题目不存在')
#     if question.state != QUEST_STATUS['正在裁定']:
#         raise JsonOutputException('暂时无法处理该题目')
#     quest_judge_data = QuestJudge.query.\
#         filter_by(state=QUEST_STATUS['正在裁定']).\
#         filter_by(quest_id=id).\
#         order_by(QuestJudge.created_at.desc()).\
#         first()
#     if quest_judge_data.operator_id != g.user.id:
#         raise JsonOutputException('该题目已被他人领取')
#     state = QUEST_STATUS['待校对']
#     quest_judge_data.state = state
#     question.state = state
#     db.session.add(quest_judge_data)
#     db.session.add(question)
#     db.session.commit()
#     return render_api({})

# # 重新输入答案
# @api_blueprint.route('/paper/answer/check/<int:id>', methods=['PUT'])
# @api_login_required
# @permission_required('JUDGE_PERMISSION')
# def check_quest(id):
#     question = Question.query.get(id)
#     if not question:
#         raise JsonOutputException('题目不存在')
#     if question.state != QUEST_STATUS['正在裁定']:
#         raise JsonOutputException('暂时无法处理该题目')
#     quest_judge_data = QuestJudge.query.\
#         filter_by(state=QUEST_STATUS['正在裁定']).\
#         filter_by(quest_id=id).\
#         order_by(QuestJudge.created_at.desc()).\
#         first()
#     if quest_judge_data.operator_id != g.user.id:
#         raise JsonOutputException('该题目已被他人领取')

#     # 题目类型
#     jieda = request.json.get('jieda', '')
#     fenxi = request.json.get('fenxi', '')
#     dianpin = request.json.get('dianpin', '')
#     kaodian = request.json.get('kaodian', '')
#     question.jieda = jieda
#     question.fenxi = fenxi
#     question.dianpin = dianpin
#     question.kaodian = kaodian
#     question.has_sub = False
#     state = QUEST_STATUS['待裁定']
#     quest_type_id = request.json.get('quest_type_id')
#     # 填空
#     if quest_type_id == '2':
#         correct_answer2 = request.json.get('correct_answer2', [])
#         if len(correct_answer2) == 0:
#             raise JsonOutputException('请输入正确答案')
#         correct_answer2 = json.dumps(correct_answer2)
#         question.correct_answer2 = correct_answer2
        
#     # 解答/选择题
#     elif quest_type_id == '3' or quest_type_id == '1':
#         correct_answer2 = request.json.get('correct_answer2', '')
#         question.correct_answer2 = correct_answer2
#         if not question.correct_answer2:
#             raise JsonOutputException('请输入正确答案')
#     # 大小题
#     elif quest_type_id == '4':
#         sub_items = request.json.get('sub_items2', [])
#         if len(sub_items) == 0:
#             raise JsonOutputException('请输入子题信息')
#         for item in sub_items:
#             item_quest_type_id = item.get('quest_type_id', 0)
#             correct_answer = item.get('correct_answer', '')
#             if correct_answer == '':
#                 raise JsonOutputException('请输入正确答案')
#             sub_quest = SubQuestion(parent_id=question.id,
#                 quest_content=item.get('quest_content', ''),
#                 quest_content_html=item.get('quest_content_html', ''),
#                 correct_answer=correct_answer,
#                 quest_no=item.get('sort', 0),
#                 qtype_id=item_quest_type_id,
#                 group=2,
#                 operator_id=g.user.id)
#             if item_quest_type_id == 1:
#                 options = item.get('options', [])
#                 option_count = len(options)
#                 # 插入选项
#                 sub_quest.qoptjson = json.dumps(options)
#                 sub_quest.option_count = option_count
#             elif item_quest_type_id == 2:
#                 correct_answer = item.get('correct_answer', [])
#                 if len(correct_answer) == 0:
#                     raise JsonOutputException('请输入正确答案')
#                 correct_answer = json.dumps(correct_answer)
#                 sub_quest.correct_answer = correct_answer
#             elif item_quest_type_id == 3:
#                 pass
#             else:
#                 raise JsonOutputException('子题题型错误')
#             db.session.add(sub_quest)
#     else:
#         raise JsonOutputException('题型错误')
#     quest_judge_data.state = state
#     question.state = state
#     db.session.add(quest_judge_data)
#     db.session.add(question)
#     db.session.commit()
#     return render_api({})