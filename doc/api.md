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