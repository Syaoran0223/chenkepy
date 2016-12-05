import json
from app.exceptions import JsonOutputException, FormValidateError
from app.decorators import api_login_required, permission_required
from app.models import Exam, User, Review, Question, QuestReviewLog, QuestLog, ExamLog, School
from app.utils import pagination
from flask import request, g, current_app
from app.const import EXAM_STATUS
from werkzeug.datastructures import MultiDict
from app.const import EXAM_STATUS,QUEST_STATUS
from . import api_blueprint
from app.models import ExamReviewLog, Question, QuestTyping
from app.utils import render_api,paginate
from app import db
from sqlalchemy import or_
import datetime


#@api_blueprint('/paper/preprocess/')
# def list_user_preprocess_file():
#     res = pagination(Exam.query.filter(Exam.state == EXAM_STATUS['预处理'] or Exam.state == EXAM_STATUS['预处理完成']).order_by(Exam.created_at.desc()))
#     items = res.get('items', [])
#     items = School.bind_auto(items, 'name')
#     res['items'] = items
#     return {
#         'code': 0,
#         'data': res
#     }

#预处理试卷列表
@api_blueprint.route('/paper/preprocess/view/<int:id>', methods=['GET'])
def view_exam_file_pre_process(id):
    data = Exam.get_exam(id)
    exam = Exam.query.get(int(id))
    examReviewLog = Review.query.filter(Review.exam_id == id,Review.reviewer_id!=g.user.id, Review.review_state==EXAM_STATUS['预处理']).all()

    if exam.state == EXAM_STATUS['预处理']:
        if len(examReviewLog) > 0:
            if examReviewLog[0].reviewer_id != g.user.id:
                raise JsonOutputException('任务已被领取')
    elif exam.state == EXAM_STATUS['已审核']:
        raise JsonOutputException('该试卷已审核')
    else:
        raise JsonOutputException('该试卷无法进行预处理')

    if len(examReviewLog) == 0:
        exam.state = EXAM_STATUS['预处理']
        exam.review_date = datetime.datetime.now()
        exam.save()
        review = Review(exam_id=exam.id, reviewer_id=g.user.id, review_state=EXAM_STATUS['预处理'], review_memo='')
        review.save()

    questList = Question.query.filter_by(exam_id=exam.id).all()

    data['quest_list'] = [item.to_dict() for item in questList]
    return {
        'code': 0,
        'data': data
    }

#添加上题目图片
@api_blueprint.route('/paper/preprocess/view',methods=['POST'])
def add_pre_review_quest_image():
    quest_no = request.json.get('quest_no')
    exam_id = request.json.get('exam_id')
    has_sub = request.json.get('has_sub')
    quest_type_id = request.json.get('quest_type_id')
    option_count = request.json.get('option_count')
    quest_image = request.json.get('quest_image')
    review_memo = request.json.get('review_memo')
    answer_image = request.json.get('answer_image')

    #添加题目数据
    res = Question.add_pre_process_quest(exam_id, quest_no, has_sub, quest_type_id, option_count, quest_image, g.user.id, review_memo, answer_image)
    #添加题目上传日志
    quest_log = QuestLog(exam_id=exam_id, quest_no=quest_no, refer_user_id=g.user.id, log_state=QuestLog['未处理'],
                         log_type='ADD')
    quest_log.save()

    #添加题目流程状态
    quest_typing = QuestTyping(exam_id=exam_id, quest_no=quest_no, reviewer_id=g.user.id,
                               review_state=QUEST_STATUS['未处理'], review_memo=review_memo)
    quest_typing.save()
    return render_api(res)

#修改题目
@api_blueprint.route('/paper/preprocess/view',methods=['PUT'])
def update_question():
    id = request.json.get('id')
    exam_id = request.json.get('exam_id')
    has_sub = request.json.get('has_sub')
    quest_type_id = request.json.get('quest_type_id')
    quest_image = request.json.get('quest_image')
    answer_image = request.json.get('answer_image')
    quest_no= request.json.get('quest_no')
    quest_content = request.json.get('quest_content')
    quest_content_html =request.json.get('quest_content_html')
    option_count = request.json.get('option_count')
    qrows = request.json.get('qrows')
    qcols = request.json.get('qcols')
    kaodian = request.json.get('kaodian')
    fenxi = request.json.get('fenxi')
    correct_answer = request.json.get('correct_answer')
    knowledge_point = request.json.get('knowledge_point')
    state = request.json.get('state')
    quest = Question.query.get(id)

    quest = Question.query.get(id)
    if quest is None:
        raise JsonOutputException('未找到题目')

    quest_type_data = QuestTyping.query.filter_by(exam_id=exam_id, quest_no=quest_no).first()

    #非未处数据不能进行修改
    if quest_type_data.oper_state != QUEST_STATUS['未处理']:
        raise JsonOutputException('该题不能修改')
    elif quest_type_data.oper_id!=g.user.id:#非本人操作无法修改
        raise JsonOutputException("您无权修改该题目")

    if has_sub is not None:
        quest.has_sub = has_sub
    if quest_type_id is not None:
        quest.quest_type_id = quest_type_id
    if quest_image is not None:
        quest.quest_image = quest_image
    if answer_image is not None:
        quest.answer_image = answer_image
    if quest_no is not None:
        quest.quest_no = quest_no
    if quest_content is not None:
        quest.quest_content = quest_content
    if quest_content_html is not None:
        quest.quest_content_html = quest_content_html
    if option_count is not None:
        quest.option_count = option_count
    if qrows is not None:
        quest.qrows = qrows
    if qcols is not None:
        quest.qcols = qcols
    if kaodian is not None:
        quest.kaodian= kaodian
    if fenxi is not None:
        quest.fenxi = fenxi
    if correct_answer is not None:
        quest.correct_answer = correct_answer
    if knowledge_point is not None:
        quest.knowledge_point= knowledge_point
    if state is not None:
        quest.state = state
    quest.save()
    quest = Question.query.get(id)
    return render_api(quest.to_dict())

@api_blueprint.route('/paper/preprocess/view/<int:id>',methods=['DELETE'])
def del_quest(id):
    quest = Question.query.get(id)
    if quest is None:
        raise JsonOutputException('未找到该试题')
    exam = Exam.query.get(quest.exam_id)
    if exam is None:
        raise JsonOutputException('未找到该试卷')

    query_type_data = QuestTyping.query.get(id)

    # 只有未处理状态数据才能被删除
    if query_type_data.oper_state != QUEST_STATUS['未处理']:
        raise JsonOutputException('该题目已进入其它处理流程,不能删除')
    elif query_type_data.oper_state == QUEST_STATUS['已删除']:  # 已删除数据不能重复删除
        raise JsonOutputException('该题目已删除')
    elif query_type_data.oper_id != g.user.id:  #非本人操作数据,不能删除
        raise JsonOutputException('您无权删除该题目')

    quest.state = QUEST_STATUS['已删除']
    quest.save()

    query_type_data.oper_state = QUEST_STATUS['已删除']
    query_type_data.save()

    return render_api('')

#查看预处理记录
@api_blueprint.route('/paper/preprocess/log', methods=['GET'])
@api_login_required
def list_quest_review_log():

    query = Review.query.filter(Review.reviewer_id != g.user.id, or_(Review.review_state == EXAM_STATUS['预处理'],\
                                                                     Review.review_state == EXAM_STATUS['预处理完成']))
    res = pagination(query)
    items = res.get('items', [])
    items = Exam.bind_auto(items, ['name', 'section', 'school_id', 'subject', 'grade', 'paper_types'])
    items = School.bind_auto(items, 'name', 'exam_school_id', 'id', 'school')
    res['items'] = items
    return render_api(res)
    # pageIndex = int(request.args.get('pageIndex', 1))
    # pageSize = int(request.args.get('pageSize', current_app.config['PER_PAGE']))
    # result = db.session.query(Question, QuestTyping, User).filter(Question.id == QuestReviewLog.exam_id,
    #                                                                  QuestReviewLog.reviewer_id == g.user.id,
    #                                                                  QuestReviewLog.review_state == EXAM_STATUS[
    #                                                                      '预处理'] or QuestReviewLog.review_state ==
    #                                                                  EXAM_STATUS[
    #                                                                      '预处理完成'] and QuestReviewLog.reviewer_id == User.id).order_by(
    #     QuestReviewLog.review_date.desc())
    # result = paginate(result, pageIndex, pageSize, error_out=False)
    # items = []
    # for item in result.items:
    #     obj = {
    #         'id': item.QuestReviewLog.id,
    #         'quest_content': item.Question.quest_content_html,
    #         'quest_no': item.Question.quest_no,
    #         'reviewer': item.User.name,
    #         'review_state': item.QuestReviewLog.review_state,
    #         'review_date': item.QuestReviewLog.review_date.strftime("%Y-%m-%d %H:%M:%S"),
    #         'review_memo': item.QuestReviewLog.review_memo
    #     }
    #     items.append(obj)
    #
    # res = {
    #     'items': items,
    #     'pageIndex': result.page - 1,
    #     'pageSize': result.per_page,
    #     'totalCount': result.total,
    #     'totalPage': result.pages
    # }
    #return res

#试卷预处理完成
@api_blueprint.route('/paper/preprocess/finish',methods=['POST'])
def finish_exam_pre_process():
    id = request.json.get("id")
    exam = Exam.query.get(id)
    review_memo = request.json.get('review_memo', '')

    review_data = Review.query.get(id)

    user_id = g.user.id
    if not exam:
        raise JsonOutputException('未找到该试卷')

    if exam.state == EXAM_STATUS['预处理']:
        if not review_data:
            if review_data.reviewer_id != user_id:
                raise JsonOutputException('非本人处理试卷,没有权限操作')
    elif exam.state == EXAM_STATUS['预处理完成']:
        raise JsonOutputException('该试卷已处理过')
    else:
        raise JsonOutputException('该试卷未处理过,不能完成')

    review_data.review_state = EXAM_STATUS['预处理完成']
    review_data.save()

    ExamLog.log(exam.id, g.user.id, EXAM_STATUS['预处理完成'], 'CONFIRM')

    exam.state = EXAM_STATUS['预处理完成']
    exam.save()
    exam = Exam.query.get(id)
    return render_api(exam.to_dict())