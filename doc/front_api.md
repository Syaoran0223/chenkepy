前端 API
======

### 登录登出

| url | method | description |
| ---- | ----- | ----- |
| /api/login/ | POST | 登录接口 |
| /api/logout/ | GET | 登出 |
| /api/register/ | POST | 注册 |

*登录接口*

    {
        "password": "123456",
        "user_name": "test1"
    }

*注册接口 参数*

    # 测试环境验证码随便填，不需要发送
    {
        "phone": "13805910002",
        "valid_code": "123456",
        "visit_code": 4444
    }

*注册详情 参数*

    {
        "phone": "13805910002",
        "email": "chenke1991@qq.com",
        "password": "123456",
        "repassword": "123456",
        "user_name": "ss",
        "school_id": "1",
        "city_id": "2",
        "grade_id": "1",
        "province_id": "1",
        "area_id": "1"
    }

### 省/市/县/学校接口

| url | method | description |
| ---- | ----- | ----- |
| /api/province | GET | 获取省份 |
| /api/city?pro_id=1257 | GET | 获取城市 |
| /api/area?city_id=1258 | GET | 获取区县 |
| /api/school?ctid=1260 | GET | 获取学校 |

### 文件上传

| url | method | description |
| ---- | ----- | ----- |
| /api/uploads | POST | 上传文件 |

`name=file`

### 试卷上传

| url | method | description |
| ---- | ----- | ----- |
| /api/paper/upload | POST | 上传试卷 |

*接口数据*

    {
        "year":"2016",
        "section":"SECOND_HALF", // FIRST_HALF 上学期 SECOND_HALF 下学期
        "province_id":"1257",
        "city_id":"1258",
        "area_id":"1260",
        "school_id":"1519",
        "grade":"10",
        "paper_types":"PAPER_UNIT",
        "subject":"GS004",
        "name":"test1",
        "exam_date":"2017-06-20",
        "attachments":[
            {
            "url":"/static/uploads/20170612/1497267955.68208742017-06-12_7.47.12.png",
            "can_preview":true,  //如果是图片填true，word填false
            "name":"屏幕快照 2017-06-12 下午7.47.12.png",
            "serverCode":0, // 填0
            "status":"success", // 填 success
            "percentage":"100%", // 填100%
            "id":"upfile_12", // 唯一id upfile_开头
            "error_msg":""
            }
        ]
    }


*静态数据*

    PAPER_TYPE = {
        'PAPER_UNIT': '单元考',
        'PAPER_MONTH': '月考',
        'PAPER_MIDLE_TERM': '半期考',
        'PAPER_LAST': '期末考',
        'PAPER_TEST': '小测',
        'PAPER_LX': '练习',
        'PAPER_HK': '会考',
        'PAPER_QULITY': '质检',
        'PAPER_MODEL': '模拟考',
        'PAPER_MIDLE': '中考',
        'PAPER_HIGH': '高考',
        'PAPER_ZZZS': '自主招生考试'
    }

    SCHOOL_YEAR = {
        '2010': '2010-2011学年',
        '2011': '2011-2012学年',
        '2012': '2012-2013学年',
        '2013': '2013-2014学年',
        '2014': '2014-2015学年',
        '2015': '2015-2016学年',
        '2016': '2016-2017学年',
        '2017': '2017-2018学年',
        '2018': '2018-2019学年',
        '2019': '2019-2020学年',
        '2020': '2020-2021学年',
        '2021': '2021-2022学年',
        '2022': '2022-2023学年',
        '2023': '2023-2024学年',
        '2024': '2024-2025学年',
        '2025': '2025-2026学年'
    }

    GRADE = {
        '1': '一年级',
        '2': '二年级',
        '3': '三年级',
        '4': '四年级',
        '5': '五年级',
        '6': '六年级',
        '7': '初一',
        '8': '初二',
        '9': '初三',
        '10': '高一',
        '11': '高二',
        '12': '高三'
    }

    SECTION = {
        'FIRST_HALF': "上学期",
        'SECOND_HALF': "下学期"
    }

    SUBJECT = {
        'GS001': '语文',
        'GS002': '数学',
        'GS003': '英语',
        'GS004': '科学',
        'GS005': '体育',
        'GS006': '音乐',
        'GS007': '美术',
        'GS008': '校本课',
        'GS017': '思品',
        'GS009': '品德与生活',
        'GS010': '品德与社会',
        'GS011': '综合实践',
        'GS012': '写字',
        'GS013': '信息',
        'GS014': '少先队活动课',
        'GS015': '心理',
        'GS016': '其他'
    }