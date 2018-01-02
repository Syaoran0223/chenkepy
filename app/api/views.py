import json, math, os
from flask import current_app, session
from PIL import Image
from flask.ext.login import login_user,logout_user,login_required,current_user
from app.exceptions import JsonOutputException, FormValidateError
from app.decorators import api_login_required, permission_required
from app.models import Attachment, Exam, User, Message
from app.utils import upload, pagination, image_save
from flask import request, g
from .forms import SmsForm, PaperUploadForm, RegisterInfoForm
from werkzeug.datastructures import MultiDict
from app.const import EXAM_STATUS, PAPER_TYPE_ORDER
from . import api_blueprint
from app.models import Region, School, ExamLog
from app.sms import SmsServer
from app.utils import render_api

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

@api_blueprint.route('/cropper', methods=['POST'])
@api_login_required
def cropper_image():
    file_url = request.json.get('file_url')
    box = request.json.get('box')
    if not file_url:
        raise JsonOutputException('请传入图片')
    if not box or len(box) != 5:
        raise JsonOutputException('切割参数错误')
    app_path = current_app.config['APP_PATH']
    file_path = '{}{}'.format(app_path, file_url)
    if not os.path.isfile(file_path):
        raise JsonOutputException('图片不存在')
    origin_image = Image.open(file_path)
    degree= -box[-1]
    box = box[0:4]
    dest_image = origin_image.rotate(degree).crop(box)
    return image_save(dest_image)

#上传试卷
@api_blueprint.route('/paper/upload', methods=['POST'])
@api_login_required
@permission_required('UPLOAD_PERMISSION')
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
                exam_date=form.exam_date.data,
                year=form.year.data,
                grade=form.grade.data,
                is_fast=form.is_fast.data,
                state=0,
                attachments=attachments,
                upload_user=g.user.id,
                order=PAPER_TYPE_ORDER[form.paper_types.data])
    result = exam.save()
    ExamLog.log(exam.id, g.user.id, EXAM_STATUS['未审核'], 'UPLOAD')
    if result.id is not None:
        return render_api({})
    raise JsonOutputException('添加失败')

#试卷列表
@api_blueprint.route('/paper/upload', methods=['GET'])
@api_login_required
@permission_required('UPLOAD_PERMISSION')
def get_exams():
    data = Exam.get_exams(g.user.id)
    return render_api(data)

#试卷明细查看
@api_blueprint.route('/paper/upload/<int:id>', methods=['GET'])
@api_login_required
@permission_required('UPLOAD_PERMISSION')
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
@permission_required('UPLOAD_PERMISSION')
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
    exam.state = EXAM_STATUS['未审核']
    exam.save()
    return render_api({})

#试卷删除
@api_blueprint.route('/paper/upload/<int:id>', methods=['DELETE'])
@api_login_required
@permission_required('UPLOAD_PERMISSION')
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

#获取用户个人信息
@api_blueprint.route('/user/info', methods=['GET'])
@api_login_required
def user_info():
    data = g.user.to_dict()
    return render_api(data)

#更新用户信息
@api_blueprint.route('/user/info', methods=['PUT'])
@api_login_required
def user_info_update():
    password = request.json.get('password')
    repassword = request.json.get('rePassword')
    valid_code = request.json.get('validCode')
    phone = request.json.get('phone')
    email = request.json.get('email')
    province_id = request.json.get('province_id', 0)
    city_id = request.json.get('city_id', 0)
    area_id = request.json.get('area_id', 0)
    school_id = request.json.get('school_id', 0)
    grade_id = request.json.get('grade_id', 0)

    user = User.query.filter_by(phone=phone).first()
    if user is not None and user.id != g.user.id:
        raise JsonOutputException('该手机号已被使用')
    if not valid_code:
        raise JsonOutputException('请输入验证码')
    sms = SmsServer()
    # 验证码验证
    if not sms.check_code(valid_code, phone):
        raise JsonOutputException('验证码错误')
    if password:
        if password != repassword:
            raise JsonOutputException('两次输入密码不一致')
        g.user.password = password
    g.user.phone = phone
    g.user.email = email
    g.user.province_id = province_id
    g.user.city_id = city_id
    g.user.area_id = area_id
    g.user.school_id = school_id
    g.user.grade_id = grade_id
    g.user.save()
    return render_api({})

# 积分记录
@api_blueprint.route('/user/score')
@api_login_required
def user_score():
    data = pagination(g.user.scores)
    return render_api(data)

@api_blueprint.route('/user/works')
@api_login_required
def user_work():
    data = g.user.get_admin_summary()
    return render_api(data)
    
# 消息记录
@api_blueprint.route('/user/message')
@api_login_required
def user_message():
    data = pagination(g.user.messages)
    message_ids = [str(item['id']) for item in data['items']]
    Message.set_is_read(message_ids)
    return render_api(data)


@api_blueprint.route('/paper/search', methods=['GET'])
def q_search():
    import http.client, urllib.parse
    import json
    httpClient = None
    pageIndex = request.args.get("pageIndex","1")
    q = request.args.get("q","")
    subject_id = request.args.get('subject_id', '')
    qtype_id = request.args.get('qtype_id', '')
    pageIndex = request.args.get('pageIndex', 0)

    size = 15
    _from = int(pageIndex) * size

    connection = http.client.HTTPConnection('search.i3ke.com', 80, timeout=10)
    headers = {'Content-type': 'application/json'}
    param = {"subject_id": subject_id, "qtype_id": qtype_id, "mlt": {"fields": "qtxt", "like": "%"+q}, "allFields": ["qtxt"], "highlightedFields": ["qtxt"],
          "from": _from, "size": size, "sort": {"_score": "desc"}}
    params = json.dumps(param)

    connection.request('POST', '/sq-apps/api/_search', params, headers)

    response = connection.getresponse()
    jsonStr = response.read().decode()
    jsonResult = json.loads(jsonStr)
    print(jsonResult)
    if jsonResult['code'] != 0:
        raise JsonOutputException('参数错误')

    res = {
        'items': jsonResult['datas'],
        'pageIndex': pageIndex,
        'pageSize': jsonResult['size'],
        'totalCount': jsonResult['total'],
        'totalPage': math.ceil(jsonResult['total']/jsonResult['size'])
    }
    return render_api(res)

@api_blueprint.route('/word')
def render_word():
    from flask.helpers import send_file
    return send_file('/Users/chenke/dev/python/information/app/static/uploads/20170208/1486552110.3344362016.docx', mimetype="application/msword", as_attachment=True)

@api_blueprint.route('/login/', methods=['POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return g.user.to_dict()
    user_name = request.json.get('user_name')
    password = request.json.get('password')
    user = User.query.filter_by(name=user_name).first()
    if user is None:
        user = User.query.filter_by(phone=user_name).first()
    if user is None:
        raise ('参数错误')('用户不存在')
    if user.verify_password(password):
        login_user(user)
        return user.to_dict()
    raise JsonOutputException('密码错误')

@api_blueprint.route('/paper/attachment/upload/<int:id>')
@login_required
@permission_required('FAST_PERMISSION')
def upload_paper_attachment(id):
    paper = Exam.query.get_or_404(id)
    if paper.is_fast != 1:
        raise JsonOutputException('操作失败')
    success = paper.push_attachments()
    if success:
        paper.is_fast = 2
        paper.save()
        return render_api({})
    raise JsonOutputException('上传失败')

@api_blueprint.route("/logout/")
@api_login_required
def logout():
    logout_user()
    return {}

@api_blueprint.route('/is_login')
@api_login_required
def is_login():
    return {
        "code": 200
    }

@api_blueprint.route('/register/', methods=['POST'])
def api_register():
    phone = request.json.get('phone')
    valid_code = str(request.json.get('valid_code', ''))
    visit_code = str(request.json.get('visit_code', ''))
    if not phone or not valid_code or not visit_code:
        raise JsonOutputException('参数错误')
    if len(phone) != 11:
        raise JsonOutputException('手机号格式错误') 
    user = User.query.filter_by(phone=phone).first()
    if user is not None:
        raise JsonOutputException('该手机号已经注册过')
    sms = SmsServer()
    if not sms.check_code(valid_code, phone):
        raise JsonOutputException('验证码错误')
    if not (len(visit_code)==4 and sum([int(i) for i in visit_code])==16):
        raise JsonOutputException('邀请码错误')
    session['phone'] = phone
    return render_api({})

@api_blueprint.route('/register/info/', methods=['POST'])
def api_register_info():
    if not session.get('phone'):
        raise JsonOutputException('请从注册页进入')
    data = MultiDict(mapping=request.json)
    form = RegisterInfoForm(data)
    if form.validate():
        user = User.query.filter_by(phone=form.phone.data).first()
        if user is not None:
            raise JsonOutputException('该手机号已经注册过')
        user = User.query.filter_by(name=form.user_name.data).first()
        if user is not None:
            raise JsonOutputException('该用户名已被使用')
        user = User(name=form.user_name.data,
            phone=form.phone.data,
            email=form.email.data,
            password=form.password.data,
            school_id=form.school_id.data,
            city_id=form.city_id.data,
            grade_id=form.grade_id.data,
            province_id=form.province_id.data,
            area_id=form.area_id.data)
        user.save()
        login_user(user)
        return render_api({})
    raise FormValidateError(form.errors)
    