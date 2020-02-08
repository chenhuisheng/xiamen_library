### 全局定义

#### 错误格式

> 业务错误

    {
        "code": 400
        "msg": "该邮箱已被注册"
    }

> 权限问题

    {
        "code": 403,
        "msg": "需要管理员权限"
    }

> 未登录

    {
        "code": 401
        "msg": "请登录后再访问"
    }

> 接口不存在

    {
        "code": 404
        "msg": "接口不存在"
    }

> 服务器错误

    {
        "code": 500
        "msg": "服务器错误"
    }

#### 查询

| 参数 | 说明 | 实例 |
| ---- | ----- | ----- |
| x_begin | 开始时间 | created_at_begin=2017-06-04 |
| x_end | 结束时间 | created_at_end=2017-06-06 |
| x_like | 模糊查询 | name_like=chenke |
| x | 查询字段 | email=chenke91@qq.com |

#### 分页结果

    {
      "items": [
        {
          
        }
      ],
      "pageIndex": 0,
      "pageSize": 20,
      "totalCount": 1,
      "totalPage": 1
    }

### 业务接口

