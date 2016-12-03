import json
from app.exceptions import JsonOutputException, FormValidateError
from app.decorators import api_login_required, permission_required
from app.models import Attachment, Exam, User, Message
from app.utils import upload, pagination
from flask import request, g, current_app
from flask.ext.login import login_required
from .forms import SmsForm, PaperUploadForm
from werkzeug.datastructures import MultiDict
from app.const import EXAM_STATUS,QUEST_STATUS
from . import api_blueprint
from app.models import Region, School, ExamReviewLog, Question, QuestReviewLog, ExamLog, Review
from app.sms import SmsServer
from app.utils import render_api,paginate
from app import db
from sqlalchemy import or_
import datetime

#试卷未审核列表
@api_blueprint.route('/paper/confirm/wait',methods=['GET'])
@api_login_required
@permission_required('CONFIRM_PERMISSION')
def listexam():
    query = Exam.query.filter(Exam.state == EXAM_STATUS['未审核'],
        Exam.upload_user!=g.user.id).order_by(Exam.created_at.desc())
    res = pagination(query)
    items = res.get('items', [])
    items = School.bind_auto(items, 'name')
    res['items'] = items
    data=Exam.list_exams(EXAM_STATUS['未审核'])
    return render_api(data)

#试卷审核 读取
@api_blueprint.route('/paper/confirm/<int:id>')
@api_login_required
@permission_required('CONFIRM_PERMISSION')
def review_exam(id):
    exam = Exam.query.get(id)
    # 超时时间
    timeout = 1800
    if not exam:
        raise JsonOutputException('试卷不存在')
    review_data = Review.query.filter_by(exam_id=exam.id).\
        filter_by(review_state=EXAM_STATUS['正在审核']).\
        first()
    #新增
    if not review_data:
        review = Review(exam_id=exam.id, reviewer_id=g.user.id,
            review_state=EXAM_STATUS['正在审核'], review_memo='')
        review.save()
        exam.state = EXAM_STATUS['正在审核']
        exam.save()
        res = exam.get_dtl()
        res['countdown'] = timeout - (datetime.datetime.now() - review.review_date).seconds
        # log
        ExamLog.log(exam.id, g.user.id, EXAM_STATUS['正在审核'], 'CONFIRM')
        return render_api(res)
    if not review_data.reviewer_id == g.user.id:
        raise JsonOutputException('该试卷已被人审核')
    countdown = timeout - (datetime.datetime.now() - review_data.review_date).seconds
    if countdown <= 0:
        review_data.review_state = EXAM_STATUS['审核超时']
        exam.state = EXAM_STATUS['未审核']
        review_data.save()
        exam.save()
        raise JsonOutputException('本次审核已过期，请重新审核')
    res = exam.get_dtl()
    res['countdown'] = timeout - (datetime.datetime.now() - review_data.review_date).seconds
    return render_api(res)
    

#试卷审核 提交、写入
@api_blueprint.route('/paper/confirm/<int:id>', methods=['PUT'])
@api_login_required
@permission_required('CONFIRM_PERMISSION')
def review_exam_update(id):
    data = MultiDict(mapping=request.json)
    state = request.json.get('state')
    memo = request.json.get('memo')
    if not state or state not in [-1, 2]:
        raise JsonOutputException('状态错误')

    #查询是否已审核
    exam = Exam.query.get(id)
    if not exam:
        raise JsonOutputException('试卷不存在')
    review_data = Review.query.filter_by(exam_id=exam.id).\
        filter_by(review_state=EXAM_STATUS['正在审核']).\
        first()
    if not review_data:
        raise JsonOutputException('审核记录不存在')
    if review_data.reviewer_id != g.user.id:
        raise JsonOutputException('改试卷已被他人审核')
    countdown = 1800 - (datetime.datetime.now() - review_data.review_date).seconds
    if countdown <= 0:
        review_data.review_state = EXAM_STATUS['审核超时']
        exam.state = EXAM_STATUS['未审核']
        review_data.save()
        exam.save()
        raise JsonOutputException('本次审核已过期，请重新审核')
    review_data.review_state = state
    review_data.review_memo = memo
    review_data.save()
    exam.state = state
    exam.save()
    ExamLog.log(exam.id, g.user.id, state, 'CONFIRM')
    return render_api({})

#登录用户审核记录
@api_blueprint.route('/examreview/list', methods=['GET'])
@api_login_required
@permission_required('CONFIRM_PERMISSION')
def list_examreview_log():
    query = Review.query.filter_by(reviewer_id=g.user.id)
    res = pagination(query)
    items = res.get('items', [])
    items = Exam.bind_auto(items, ['name', 'section', 'school_id', 'subject', 'grade', 'paper_types'])
    items = School.bind_auto(items, 'name', 'exam_school_id', 'id', 'school')
    res['items'] = items
    return render_api(res)