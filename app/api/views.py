import json
from app.exceptions import JsonOutputException, FormValidateError
from app.decorators import api_login_required
from app.models import Attachment, Exam
from app.utils import upload, pagination
from flask import request, g
from flask.ext.login import login_required
from .forms import SmsForm, PaperUploadForm
from werkzeug.datastructures import MultiDict
from app.const import EXAM_STATUS
from . import api_blueprint
from app.models import Region, School, ExamReviewLog
from app.sms import SmsServer

import datetime
@api_blueprint.route('/province')
def province():
    title = request.args.get('title', '')
    provinces = Region.get_province(title)
    return {
        'code': 0,
        'data': provinces
    }

@api_blueprint.route('/city')
def city():
    pro_id = request.args.get('pro_id')
    title = request.args.get('title', '')
    if not pro_id:
        raise JsonOutputException('need pro_id')
    cities = Region.get_city(pro_id, title)
    return {
        'code': 0,
        'data': cities
    }

@api_blueprint.route('/area')
def area():
    city_id = request.args.get('city_id')
    title = request.args.get('title', '')
    if not city_id:
        raise JsonOutputException('need city_id')
    areas = Region.get_area(city_id, title)
    return {
        'code': 0,
        'data': areas
    }

@api_blueprint.route('/school')
def school():
    ctid = request.args.get('ctid')
    title = request.args.get('title', '')
    if not ctid:
        raise JsonOutputException('need ctid')
    schools = School.get_schools_by_ctid(ctid, title)
    return {
        'code': 0,
        'data': schools
    }

@api_blueprint.route('/sms')
def send_msg():
    form = SmsForm(request.args)
    if not form.validate():
        raise FormValidateError(form.errors)
    phone = form.phone.data
    sms = SmsServer()
    success, code = sms.generate_code(phone)
    if not success:
        return {
            'code': 15,
            'msg': '请求太频繁，请稍后重试'
        }
    return sms.send_code(code, phone)


@api_blueprint.route('/uploads', methods=['POST'])
@api_login_required
def upload_attachment():
    file = request.files.get('file')
    thumb = bool(request.args.get('thumb', False))
    if not file:
        raise JsonOutputException('请选择要上传的文件')
    file_type = request.form.get('type', '')
    data = upload(file, thumb)
    if data.get('status') is True:
        attachment = Attachment(
            name=data.get('original', ''),
            url=data.get('url', ''),
            user_id=g.user.id,
            file_type=file_type)
        attachment.save()
        #attachment.id
        return {
            'code': 0,
            'data': [attachment.url]
        }
    raise JsonOutputException('上传失败')

#上传试卷
@api_blueprint.route('/paper/upload', methods=['POST'])
@api_login_required
def paper_upload():
    data = MultiDict(mapping=request.json)
    form = PaperUploadForm(data)
    if not form.validate():
        raise FormValidateError(form.errors)
    # todo 插入数据库
    attachments = request.json.get('attachments', [])
    exam = Exam(name=form.name.data, section=form.section.data, subject=form.subject.data, paper_types=form.paper_types.data, \
                province_id=form.province_id.data, city_id=form.city_id.data, area_id=form.area_id.data,\
                school_id=form.school_id.data,
                year=form.year.data, grade=form.grade.data, state=0, attachments=attachments, upload_user=g.user.id)
    result = exam.save()
    if result.id is not None:
        return {
            'code': 0,
            'data': ''
        }
    raise JsonOutputException('添加失败')

#试卷列表
@api_blueprint.route('/paper/upload', methods=['GET'])
@api_login_required
def get_exams():
    data = Exam.get_exams(g.user.id)
    return {
        'code': 0,
        'data': data
    }

#试卷明细查看
@api_blueprint.route('/paper/upload/<int:id>', methods=['GET'])
@api_login_required
def get_exam(id):
    data = Exam.get_exam(id)
    if data is not None:
        return {
            'code': 0,
            'data': data
        }
    else:
        raise JsonOutputException('没有数据')

#试卷更新
@api_blueprint.route('/paper/upload/<int:id>', methods=['PUT'])
@api_login_required
def update_exam(id):
    data = MultiDict(mapping=request.json)
    form = PaperUploadForm(data)
    if not form.validate():
        raise FormValidateError(form.errors)
    attachments = request.json.get('attachments', [])
    exam = Exam.query.get(int(id))
    exam.name = form.name.data
    exam.section = form.section.data
    exam.subject = form.subject.data
    exam.paper_types = form.paper_types.data
    exam.province_id = form.province_id.data
    exam.city_id = form.city_id.data
    exam.area_id = form.area_id.data
    exam.school_id = form.school_id.data
    exam.year = form.year.data
    exam.grade = form.grade.data
    exam.attachments = attachments
    exam.save()
    if data is not None:
        return {
            'code': 0,
            'data': data
        }
    else:
        raise JsonOutputException('更新失败')

#试卷删除
@api_blueprint.route('/paper/upload/<int:id>', methods=['DELETE'])
@api_login_required
def delexam(id):

    exam = Exam.query.get(int(id))
    if exam is None or exam.state > EXAM_STATUS['未审核']:
        raise JsonOutputException('删除失败')
    else:
        exam.state = EXAM_STATUS['已删除']
        exam.save()
        return {
            'code': 0,
            'data': ''
        }
#试卷未审核列表
@api_blueprint.route('/paper/confirm/wait',methods=['GET'])
@api_login_required
def listexam():
    data = Exam.list_exams(EXAM_STATUS['未审核'])
    return {
            'code': 0,
            'data': data
    }

#试卷审核 读取
@api_blueprint.route('/paper/confirm/review/<int:id>', methods=['GET'])
@api_login_required
def review_exam(id):
    data = Exam.get_exam(id)
    #审核倒计时 30分钟 （秒）
    data['countdown'] = 1800
    #更新审核
    exam = Exam.query.get(int(id))
    examReviewLog = ExamReviewLog.query.filter(ExamReviewLog.exam_id == exam.id, ExamReviewLog.review_state == EXAM_STATUS['正在审核'] ).order_by(ExamReviewLog.created_at.desc())
    examReviewLog = examReviewLog.all()

    #正在审核状态
    if exam.state == EXAM_STATUS['正在审核']:
        #并且不为本人操作
        if len(examReviewLog) > 0:
            if examReviewLog[0].reviewer_id != g.user.id:
                raise JsonOutputException('任务已被领取')
            else:
                data['countdown'] = 1800 - (datetime.datetime.now() - examReviewLog[0].review_date).seconds;

    exam.state = EXAM_STATUS['正在审核']
    exam.review_date = datetime.datetime.now()
    exam.save()

    if len(examReviewLog) == 0:
        examReview = ExamReviewLog(exam_id = exam.id, reviewer_id = g.user.id, review_state = EXAM_STATUS['正在审核'],review_memo='')
        examReview.save()

    return {
            'code': 0,
            'data': data
    }

#试卷审核 提交、写入
@api_blueprint.route('/paper/confirm/review/<int:id>', methods=['PUT'])
@api_login_required
def review_exam_update(id):
    data = MultiDict(mapping=request.json)
    if data['state'] is None or data['state']=='':
        raise JsonOutputException('缺少审核结果,审核失败')
    examReviewLog = ExamReviewLog.query.filter(ExamReviewLog.reviewer_id == g.user.id, ExamReviewLog.exam_id == id,\
                                               ExamReviewLog.review_state == EXAM_STATUS['正在审核']).all()
    if len(examReviewLog) == 0:
        raise JsonOutputException('已审核过，不能重复审核')
    if (datetime.datetime.now() - examReviewLog[0].review_date).seconds > 1800:
        raise JsonOutputException('超过审核时间')

    examReviewLog = examReviewLog[0]
    examReviewLog.review_date = datetime.datetime.now()
    examReviewLog.review_memo = data['memo']
    examReviewLog.reviewer_id = g.user.id
    examReviewLog.review_state = data['state']
    examReviewLog.save()

    exam = Exam.query.get(int(id))
    exam.state = data['state']
    exam.review_date = datetime.datetime.now()
    exam.save()

    return {
        'code': 0,
        'data': ''
    }

#登录用户审核记录
@api_blueprint.route('/examreview/list', methods=['GET'])
@api_login_required
def list_examreview_log():
    return ExamReviewLog.list_log(g.user.id)

