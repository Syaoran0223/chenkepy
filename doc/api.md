API 规范
======

### 后台人员管理

| url | method | description | code |
| ---- | ----- | ----- | ---- |
| /admin/admin | GET | 获取所有人员 | 200 |
| /admin/admin/1 | GET | 获取1号人员 | 200 |
| /admin/admin | POST | 新增 | 201 |
| /admin/admin/1 | PUT | 修改1号人员 | 200 |
| /admin/admin/1 | DELETE | 删除1号人员 | 202 |

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