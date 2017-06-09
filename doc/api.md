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

### 试卷详情

`/admin/exams/<id>`

    "question": {
      "answer_image": [],   //答案图片
      "answer_list1": [],   //校对前答案列表->填空题
      "answer_list2": [],   //校对后答案列表
      "correct_answer": null,   //正确答案
      "correct_answer1": null,  //校对前的正确答案
      "correct_answer2": null,  //校对后的正确答案
      "created_at": "2017-01-18 21:17:49",
      "dianpin": null,  //点评
      "exam_id": 10,
      "fenxi": null,    //分析
      "has_sub": 1,     //是否有子题
      "id": 18,
      "insert_user_id": 1,
      "jieda": "<p>asdasd</p>\n",   //解答
      "kaodian": null,  //考点
      "knowledge_point": null,  //知识点
      "option_count": 0,    //选项数
      "options1": [],   //校对前的选项列表->选择题
      "options2": [],   //校对后的选项列表->选择题
      "order": 0,
      "qcols": null,    //选项行数->选择题
      "qrows": null,    //选项列数->选择题
      "quest_content": "aaaaaaaaa", //题目内容
      "quest_content_html": "<p>aaaaaaaaa</p>\n",   //题目内容
      "quest_image": [],    //题目图片
      "quest_no": 1,    //题号
      "quest_type_id": "1", //题型 1选择题 2填空题 3解答题
      "refer_quest_id": 0,  //题库系统的id
      "state": 99,  // 题目状态: '已删除': -99, '未处理': 0, '正在录题': 1, '审核不通过': 2, '完成录题': 3, '正在解答': 4, '完成解答': 5, '正在检查': 6, '待裁定': 7, '正在裁定': 8, '待校对': 9, '正在校对': 10, '结束录题': 99
      "sub_items1": [   //校对前的子题
        {
          "_id": "sub_item_47",
          "answer_list": [],
          "correct_answer": "A",
          "finish_state": "answer",
          "operator_id": 1,
          "options": [
            {
              "_id": "option_50",
              "_selected": true,
              "content": "<p>aaa</p>\n",
              "sort": "A"
            },
            {
              "_id": "option_51",
              "_selected": false,
              "content": "<p>bbbbbb</p>\n",
              "sort": "B"
            },
            {
              "_id": "option_52",
              "_selected": false,
              "content": "<p>ccccc</p>\n",
              "sort": "C"
            }
          ],
          "quest_answer": "",
          "quest_content": "aaaaaaa",
          "quest_content_html": "<p>aaaaaaa</p>\n",
          "quest_option_html": "",
          "quest_type_id": "1",
          "sort": 1
        },
        {
          "_id": "sub_item_53",
          "answer_list": [
            {
              "_id": "b_answer_58",
              "content": "<p>aaaa</p>\n"
            },
            {
              "_id": "b_answer_59",
              "content": "<p>bbbb</p>\n"
            }
          ],
          "correct_answer": [
            "<p>aaaa</p>\n",
            "<p>bbbb</p>\n"
          ],
          "finish_state": "answer",
          "operator_id": 1,
          "options": [],
          "quest_answer": "",
          "quest_content": "asdasdasd",
          "quest_content_html": "<p>asdasdasd</p>\n",
          "quest_option_html": "",
          "quest_type_id": "2",
          "sort": 2
        },
        {
          "_id": "sub_item_54",
          "answer_list": [],
          "correct_answer": "<p>asdasdadd</p>\n",
          "finish_state": "answer",
          "operator_id": 1,
          "options": [],
          "quest_answer": "<p>asdasdadd</p>\n",
          "quest_content": "cdcasdasd",
          "quest_content_html": "<p>cdcasdasd</p>\n",
          "quest_option_html": "",
          "quest_type_id": "3",
          "sort": 3
        }
      ],
      "sub_items2": [   //校对后的子题
        {
          "_id": "sub_item_47",
          "answer_list": [],
          "correct_answer": "B",
          "finish_state": "answer_check",
          "operator_id": 1,
          "options": [
            {
              "_id": "option_50",
              "_selected": false,
              "content": "<p>aaa</p>\n",
              "sort": "A"
            },
            {
              "_id": "option_51",
              "_selected": true,
              "content": "<p>bbbbbb</p>\n",
              "sort": "B"
            },
            {
              "_id": "option_52",
              "_selected": false,
              "content": "<p>ccccc</p>\n",
              "sort": "C"
            }
          ],
          "quest_answer": "",
          "quest_content": "aaaaaaa",
          "quest_content_html": "<p>aaaaaaa</p>\n",
          "quest_option_html": "",
          "quest_type_id": "1",
          "sort": 1
        },
        {
          "_id": "sub_item_53",
          "answer_list": [
            {
              "_id": "b_answer_58",
              "content": "<p>aaaa</p>\n"
            },
            {
              "_id": "b_answer_59",
              "content": "<p>bbbb</p>\n"
            }
          ],
          "correct_answer": [
            "<p>aaaa</p>\n",
            "<p>bbbb</p>\n"
          ],
          "finish_state": "answer_check",
          "operator_id": 1,
          "options": [],
          "quest_answer": "",
          "quest_content": "asdasdasd",
          "quest_content_html": "<p>asdasdasd</p>\n",
          "quest_option_html": "",
          "quest_type_id": "2",
          "sort": 2
        },
        {
          "_id": "sub_item_54",
          "answer_list": [],
          "correct_answer": "<p>asdasdadd</p>\n",
          "finish_state": "answer_check",
          "operator_id": 1,
          "options": [],
          "quest_answer": "<p>asdasdadd</p>\n",
          "quest_content": "cdcasdasd",
          "quest_content_html": "<p>cdcasdasd</p>\n",
          "quest_option_html": "",
          "quest_type_id": "3",
          "sort": 3
        }
      ],
      "updated_at": "2017-01-18 21:21:31"
    }
