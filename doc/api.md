API 规范
======

### 登录登出

| url | method | description |
| ---- | ----- | ----- |
| /admin/login | GET | 登录页 |
| /admin/login | POST | 登录接口 |
| /admin/logout | GET | 登出 |

*登录接口*

    {
        "password": "123456",
        "phone": "18558707091"
    }


### 省市县接口

| url | method | description |
| ---- | ----- | ----- |
| /api/province | GET | 获取省份 |
| /api/city?pro_id=20 | GET | 获取城市 |
| /api/area?city_id=2 | GET | 获取区 |


### 后台人员管理

| url | method | description |
| ---- | ----- | ----- |
| /admin/admins | GET | 获取所有人员 |
| /admin/admins/1 | GET | 获取1号人员 |
| /admin/admins | POST | 新增 |
| /admin/admins/1 | PUT | 修改1号人员 |
| /admin/admins/1 | DELETE | 删除1号人员 |

*实例*

    {
      "created_at": "2017-03-20 22:23:27",
      "email": null,
      "id": 2,
      "name": "chenke91",
      "phone": "18558707091",
      "search_fields": [    //搜索条件
        "name_like",
        "phone_like",
        "state",
        "created_at_begin",
        "created_at_end"
      ],
      "state": 0,
      "updated_at": "2017-03-20 22:23:27"
    }


### 前台人员管理

| url | method | description |
| ---- | ----- | ----- |
| /admin/users | GET | 获取所有人员 |
| /admin/users/1 | GET | 获取1号人员 |
| /admin/users/1 | PUT | 修改1号人员(只允许修改 permissions字段) |

*实例*

    {
        "area_id": 1266,
        "area_name": "连江县",
        "city_id": 1258,
        "city_name": "福州市",
        "created_at": "2016-12-26 21:34:56",
        "email": "chenke91@gmail.com",
        "grade_id": 11,
        "id": 2,
        "name": "test2",
        "permissions": [
            "UPLOAD_PERMISSION"
        ],
        "phone": "18559131924",
        "province_id": 1257,
        "province_name": "福建省",
        "school_id": 1532,
        "school_name": "尚德中学",
        "search_fields": [      //搜索字段
            "name_like",
            "phone_like",
            "state",
            "created_at_begin",
            "created_at_end",
            "school_id",
            "grade_id",
            "city_id",
            "province_id",
            "area_id",
            "permissions_like"
        ],
        "state": 0,
        "updated_at": "2016-12-26 21:34:56",
        "user_type": null
    }

### 个人工作统计

| url | method | description |
| ---- | ----- | ----- |
| /admin/users/statistic | GET | 获取个人工作统计 |

`/admin/users/statistic`

*参数*

    user_id
    begin_time
    end_time
    time_type: `HOUR` `MONTH` `DATE`
    statistic_type: 
        `UPLOAD_PERMISSION` 上传
            state:
                `ready` 待审核
                `confirming` 正在审核
                `pass`  审核通过
                `useage`    采纳
        `CONFIRM_PERMISSION` 审核
            state:
                `reject`    审核不通过
                `confirming` 正在审核
                `pass` 审核通过
                `usage` 采纳
        `DEAL_PERMISSION` 预处理
            state:
                `dealing` 正在处理
                `complete` 处理结束
        `INPUT_PERMISSION`  录题
            state:
                `complete` 完成录题
                `complete_answer` 完成解答
                `finish` 结束录题
                `typing` 正在录题
        `ANSWER_PERMISSION` 解答
            state:
                `answering` 正在解答
                `complete_answer` 完成解答
        `CHECK_PERMISSION` 检查
            state:
                `checking` 正在检查
                `complete` 完成检查
        `JUDGE_PERMISSION` 裁定
            state:
                `judging` 正在裁定
                `complete` 完成裁定
        `VERIFY_PERMISSION` 校对
            state:
                `verifying` 正在校对
                `completes` 完成校对
                
### 试卷管理

| url | method | description |
| ---- | ----- | ----- |
| /admin/exams | GET | 获取试卷列表 |
| /admin/exams/statistic | GET | 获取试卷列表 |


`/admin/exams/statistic`

*参数*

    begin_time
    end_time
    province_id
    city_id
    area_id
    school_id
    grade
    statistic_type  统计类型
        `paper_types` 类型统计
        `state` 状态统计
        `subject` 学科统计
        `grade` 年级统计

### 题目管理

| url | method | description |
| ---- | ----- | ----- |
| /admin/questions | GET | 获取试卷列表 |
| /admin/questions/statistic | GET | 获取试卷列表 |


`/admin/questions/statistic`

*参数*

    begin_time
    end_time
    province_id
    city_id
    area_id
    school_id
    grade
    statistic_type  统计类型
        `quest_type_id` 题型统计
        `state` 状态统计
        `subject` 学科统计
        `grade` 年级统计

### 工作统计列表

`/admin/users/works`
