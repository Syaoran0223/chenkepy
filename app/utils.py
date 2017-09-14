# coding: utf-8

from flask import current_app, request, g
# from PIL import Image
from .exceptions import ValidationError, JsonOutputException
from werkzeug import secure_filename
from datetime import datetime, timedelta, date
from random import randint
import os, time, requests, json, hashlib, math
from flask.ext.sqlalchemy import BaseQuery
import json

def allowed_file(filename, allow_extensions):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in allow_extensions

default_extensions = set(['png', 'jpg', 'jpeg', 'gif',
    'PNG', 'JPG', 'JPEG', 'GIF', 'pdf', 'PDF', 'doc', 'DOC', 'docx', 'DOCX'])

def upload(file, thumb=False, allow_extensions=default_extensions):
    sub_folder = datetime.today().strftime('%Y%m%d')
    upload_folder = os.path.join(current_app.static_folder, 'uploads/{}'.format(sub_folder))
    if not os.path.isdir(upload_folder):
        os.mkdir(upload_folder)
    if file and allowed_file(file.filename, allow_extensions):
        original = secure_filename(file.filename)
        if original in default_extensions:
            original = '.' + original
        filename = str(time.time()) + original
        file_static = '/static/uploads/{}/'.format(sub_folder) + filename
        real_file = os.path.join(upload_folder, filename)
        file.save(real_file)
        res = {
            "status": True,
            "url": file_static,
            "title": original,
            "original": original
        }
        return res
    return {'status': False}

def image_save(image):
    sub_folder = datetime.today().strftime('%Y%m%d')
    upload_folder = os.path.join(current_app.static_folder, 'uploads/{}'.format(sub_folder))
    if not os.path.isdir(upload_folder):
        os.mkdir(upload_folder)
    filename = str(time.time()) + '.png'
    file_static = '/static/uploads/{}/'.format(sub_folder) + filename
    real_file = os.path.join(upload_folder, filename)
    image.save(real_file)
    return {
        "code": 0,
        "data": {
            "url": file_static
        }
    }


# def get_thumb(filename):
#     path, ext = os.path.splitext(filename)
#     thumb_file = '{}_thumb{}'.format(path, ext)
#     if os.path.isfile(thumb_file):
#         return thumb_file.replace(current_app.static_folder, '/static')
#     size = (150, 150)
#     try:
#         img = Image.open(filename)
#         img.thumbnail(size)
#         img.save(thumb_file)
#         return thumb_file.replace(current_app.static_folder, '/static')
#     except IOError:
#         return None


# md5加密
def generate_password_hash(password):
    password_hash = hashlib.md5()
    password_hash.update(password.encode('utf-8'))
    return password_hash.hexdigest()

md5 = generate_password_hash

# 检查密码是否正确
def check_password_hash(password_hash, password):
    password_hash2 = hashlib.md5()
    password_hash2.update(password.encode('utf-8'))
    return password_hash == password_hash2.hexdigest()


def paginate(sa_query, page, per_page=20, error_out=True):
    sa_query.__class__ = BaseQuery
    # We can now use BaseQuery methods like .paginate on our SA query
    return sa_query.paginate(page, per_page, error_out)

def pagination(query, ignore=None, to_dict=True):
    page = int(request.args.get('pageIndex', 0))
    pageSize = int(request.args.get('pageSize', current_app.config['PER_PAGE']))
    data = query.paginate(page+1, pageSize, error_out=False)
    items = []
    for item in data.items:
        if ignore and isinstance(ignore, list):
            for field in ignore:
                item.__dict__.pop(field)

        if not to_dict:
            items.append(item)
        else:
            items.append(item.to_dict())

    res = {
        'items': items,
        'pageIndex': data.page - 1,
        'pageSize': data.per_page,
        'totalCount': data.total,
        'totalPage': data.pages
    }
    return res

def get_today():
    today = datetime.today()
    today_str = '{}{}{}'.format(today.year, today.month, today.day)
    return today_str


def _add_month_interval (dt,inter):
    m=dt.month+inter-1
    y=dt.year+math.floor(m/12)
    m=m % 12 +1
    return (y,m)

def add_month_interval (dt,inter):
    y,m=_add_month_interval(dt,inter)
    y2,m2=_add_month_interval(dt,inter+1)
    maxD=( date(y2,m2,1) - timedelta(days=1) ).day
    d= dt.day<=maxD and dt.day or maxD
    return date(y,m,d)

def add_year_interval (dt,inter):
    return add_month_interval(dt,inter*12)

def render_api(data):
    return {
        'code': 0,
        'data': data
    }

def get_i3ke_token():
    url = "http://www.i3ke.com/api/v2/user/auth"
    headers = {'content-type': 'application/json'}
    payload = {
        "mobile": "18558707091",
        "password": "chenke91.com",
        "expire_hour": 1
    }
    payload = json.dumps(payload)
    result = requests.post(url, data=payload, headers=headers)
    if not result.ok:
        raise JsonOutputException('请求失败')
    res = result.json()
    if res['ok']:
        return 'Bearer ' + res['data']['login_token']
    raise JsonOutputException('获取token失败！')

def post_paper_to_i3ke(data):
    url = "http://www.i3ke.com/api/v2/papers/famous"
    headers = {
        'content-type': "application/json;charset=UTF-8",
        'authorization': get_i3ke_token()
    }
    data = json.dumps(data)
    response = requests.post(url, data=data, headers=headers)
    if not response.ok:
        raise JsonOutputException('请求失败')
    res = response.json()
    if not res['ok']:
        raise JsonOutputException(res['err'])
    return res['data']['papers']['id']

def put_paper_attachment_to_i3ke(paper_id, file_path, num):
    url = 'http://www.i3ke.com/api/v2/papers/famous/id/{}/pics/{}'.format(paper_id, num)
    headers = {
        'content-type': "application/octet-stream",
        'authorization': get_i3ke_token()
    }
    data = open(file_path, 'rb').read()
    response = requests.put(url=url, data=data, headers=headers)
    if not response.ok:
        raise JsonOutputException('试卷上传失败')
    res = response.json()
    if not res['ok']:
        raise JsonOutputException('试卷上传被拒绝')
    return True


    