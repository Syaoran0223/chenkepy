API 规范
======

### 请求类型

| type | description |
| ----- | ----- |
| GET | 获取数据 |
| POST | 新建数据 |
| PUT | 更新数据 |
| DELETE | 删除数据 |

### 请求示例

*以article为例，说明增删改查的API定义*

| url | method | description | code |
| ---- | ----- | ----- | ---- |
| /api/v1/articles | GET | 获取所有文章列表 | 200 |
| /api/v1/articles/1 | GET | 获取1号文章 | 200 |
| /api/v1/articles/1/tags | GET | 获取1号文章的标签 | 200 |
| /api/v1/articles/1/tags/1 | GET | 获取1号文章的1号标签 | 200 |
| /api/v1/articles | POST | 添加文章 | 201 |
| /api/v1/articles/1 | PUT | 修改1号文章 | 200 |
| /api/v1/articles/1 | DELETE | 删除1号文章 | 202 |

*注意点:*

- URL中的对象定义为复数形式，如 `/api/v1/articles`中使用`articles`而不是`article`

### 请求参数规范

1. 按时间查询参数规范

    | argument | description |
    | ------- | ------ |
    | start | 开始时间 |
    | end | 结束时间 |


2. 分页参数规范

    | argument | description |
    | ---- | ---- |
    | per_page | 每页条数 |
    | page | 查询页码 |
    
3. 欢迎补充

### 响应格式规范

`/api/v1/articles/1` 获取对象 `GET` `code: 200`

    {
        id: 1,
        title: 'this is title',
        body: 'this is body'
    }

`/api/v1/articles` 获取列表 `GET` `code: 200`

    {
        items: [
            {},
            {},
        ]
        pagination: {
            count: 200,
            page: 4,
            per_page: 10,
            total_page: 20
        }
    }
    
`/api/v1/articles` 新增文章 `POST` `code: 201`

    {
        id: 101,
        title: 'this is new title',
        body: 'this is new body'
    }  //返回新增的对象
    
`/api/v1/articles/101` 修改文章 `PUT` `code: 200`

    {
        id: 101,
        title: 'this is updated title',
        body: 'this is new body'
    }  //返回修改的对象

`/api/v1/articles/101` 删除文章 `DELETE` `code: 202`

    {}    //删除的返回码为202， 返回内容为空
    
    
### 错误格式规范

1. 错误类型

    | type | code | description |
    | ----- | ----- | ----- |
    | Unauthorized | 401 | 未登录 |
    | Forbidden | 403 | 权限不足 |
    | Conflict | 409 | 操作失败, 如用户名重复，余额不足之类的，前端可将该状态的错误信息显示给用户 |
    | Bad Request | 400 | 请求参数不合法 |
    | Not Found | 404 | 请求的资源不存在 |
    | Internal Server Error | 500 | 服务器端错误 |
    
2. 错误示例

    `Unauthorized` `401`
        
        {status: 'Unauthorized', message: '未登录'}
        
    `Forbidden` `403`
    
        {status: 'Forbidden', message: '无此权限'}
        
    `Conflict` `409`
    
        {status: 'Conflict', message: '用户名已存在'}
        
    `Bad Request` `400`
    
        {status: 'Bad Request', message: 'argument name is required'}
        
    `Not Found` `404`
        
        {status: 'Not Found', message: 'resource not found'}
        
    `Internal Server Error` `500`
    
        {status: 'Internal Server Error', message: 'something wrong in server'}
        
### 前后端交互说明

1. 每次请求后端直接将结果返回给前端，返回结果中不包含响应的状态，前端可根据响应码判断请求是否成功。

2. 成功的响应码为2开头，包括：
    - 200 查询成功，修改成功
    - 201 创建成功
    - 202 删除成功
    
3. 失败的响应码为4开头，包括：
    - 400 参数错误
    - 401 未登录
    - 403 权限不足
    - 404 not found
    - 409 业务层面的错误，如余额不足，用户名已存在等
    

