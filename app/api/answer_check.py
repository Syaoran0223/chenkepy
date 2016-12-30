import json, math
from app import db
from app.exceptions import JsonOutputException
from app.decorators import api_login_required, permission_required
from app.utils import upload, pagination
from flask import request, g
from app.const import QUEST_STATUS
from . import api_blueprint
from app.models import Question, QuestCheck, QOption, SubQuestion
from app.utils import render_api
import datetime

#待检查列表
@api_blueprint.route('/paper/answer/check/wait',methods=['GET'])
@api_login_required
@permission_required('CHECK_PERMISSION')
def answer_check_wait():
    data = Question.get_quest_by_state(QUEST_STATUS['完成解答'])
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
    query = QuestCheck.query.\
        filter_by(operator_id=g.user.id)
    res = pagination(query, None, False)
    items = [item.get_question_dtl() for item in res['items']]
    res['items'] = items
    return render_api(res)

# # 题目解答
# @api_blueprint.route('/paper/answer/<int:id>', methods=['PUT'])
# @api_login_required
# @permission_required('CHECK_PERMISSION')
# def answer_quest(id):
#     question = Question.query.get(id)
#     if not question:
#         raise JsonOutputException('题目不存在')
#     if question.state != QUEST_STATUS['正在解答']:
#         raise JsonOutputException('暂时无法处理该题目')
#     quest_answer_data = QuestAnswer.query.\
#         filter_by(state=QUEST_STATUS['正在解答']).\
#         filter_by(quest_id=id).\
#         order_by(QuestAnswer.created_at.desc()).\
#         first()
#     if quest_answer_data.operator_id != g.user.id:
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
#     state = QUEST_STATUS['完成解答']
#     quest_type_id = request.json.get('quest_type_id')
#     # 选择题
#     if quest_type_id == '1':
#         options = request.json.get('options', [])
#         correct_answer = request.json.get('correct_answer', '')
#         if not correct_answer:
#             raise JsonOutputException('请输入正确答案')
#         question.correct_answer = correct_answer
#         # 修改选项选中状态
#         for data in options:
#             option = QOption.query.get(data.get('id', 0))
#             if option:
#                 option.qok = data['_selected']
#                 db.session.add(option)
#     # 填空
#     elif quest_type_id == '2':
#         correct_answer = request.json.get('correct_answer', [])
#         if len(correct_answer) == 0:
#             raise JsonOutputException('请输入正确答案')
#         correct_answer = json.dumps(correct_answer)
#         question.correct_answer = correct_answer
        
#     # 解答
#     elif quest_type_id == '3':
#         correct_answer = request.json.get('quest_answer', '')
#         question.correct_answer = correct_answer
#         if question.correct_answer == '':
#             raise JsonOutputException('请输入正确答案')
#     # 大小题
#     elif quest_type_id == '4':
#         sub_items = request.json.get('sub_items', [])
#         if len(sub_items) == 0:
#             raise JsonOutputException('请输入子题信息')
#         for item in sub_items:
#             sub_quest = SubQuestion.query.get(item.get('id', 0))
#             if not sub_quest:
#                 continue
            
#             correct_answer = item.get('correct_answer', '')
#             if correct_answer == '':
#                 raise JsonOutputException('子题({})请输入正确答案'.format(sub_quest.quest_no))
#             sub_quest.correct_answer = correct_answer
#             if sub_quest.qtype_id == 2:
#                 correct_answer = item.get('correct_answer', [])
#                 if len(correct_answer) == 0:
#                     raise JsonOutputException('子题({})请输入正确答案'.format(sub_quest.quest_no))
#                 correct_answer = json.dumps(correct_answer)
#                 sub_quest.correct_answer = correct_answer
#             db.session.add(sub_quest)
#     else:
#         raise JsonOutputException('题型错误')
#     quest_answer_data.state = state
#     question.state = state
#     db.session.add(quest_answer_data)
#     db.session.add(question)
#     db.session.commit()
#     return render_api({})