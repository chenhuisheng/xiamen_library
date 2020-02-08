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

#### header请求参数

    header: {
            "Device-Code": ""   //设备号
        }

### 业务接口

#### HOST

`dev.xiamen.chaoxingbook.com`

#### 登录

> 登录

`(POST) /api/client/login`

*参数*

    {
        "phone": "13763812345",
        "password": "123456"
    }

#### 专题管理

> 获取专题列表

`(GET) /api/client/projects`

*正确时返回*

    {
        "code": 200,
        "data": [
            {
                "id": 10,
                "title": "测试专题88"
            },
            {
                "id": 11,
                "title": "a"
            }
        ],
        "msg": ""
    }

> 获取专题图书

`(GET) /api/client/device/project_books`

*错误(未传Device-Code)时返回*

    {
        "code": 401,
        "msg": "请输入Device-Code"
    }

*错误(无设备或无专题)时返回*

    {
        "code": 401,
        "msg": "设备未配置"
    }

*正确时返回*

    {
        "code": 200,
        "data": {
            "items": [
                {
                    "author": "作者",
                    "catalog": "目录",
                    "catalog_json": [],
                    "created_at": "2018-11-06 11:19:38",
                    "file_path": "/mnt/g/xiamen_library/src/app/resource/uploads/images/20181103/1541230286.66042111.pdf",
                    "file_size": 0,
                    "file_type": "pdf",
                    "id": 34,
                    "image": "/mnt/g/xiamen_library/src/app/resource/uploads/images/20181103/1541230176.797511.jpg",
                    "is_delete": false,
                    "isbn": "1234567",
                    "pages": 15,
                    "pub_date": "1970-01-01",
                    "publisher": "出版社",
                    "summary": "摘要",
                    "title": "我不笑",
                    "updated_at": "2018-11-06 11:47:44"
                },
            ]
        },
        "msg": ""
    }

> 获取专题轮播图

`(GET) /api/client/device/project_pictures`

*错误(未传Device-Code)时返回*

    {
        "code": 401,
        "msg": "请输入Device-Code"
    }

*错误(无设备或无专题)时返回*

    {
        "code": 401,
        "msg": "设备未配置"
    }

*正确时返回*

    {
        "code": 200,
        "data": [
            {
                "created_at": "2018-11-03 15:14:49",
                "id": 1,
                "is_delete": false,
                "summary": "123456",
                "title": "11111",
                "updated_at": "2018-11-05 15:14:04",
                "url": "/mnt/g/xiamen_library/src/app/resource/uploads/images/20181103/1541230176.797511.jpg"
            }
        ],
        "msg": ""
    }

> 获取当前设备所选专题

`(GET) /api/client/device/projects`

*错误(未传Device-Code)时返回*

    {
        "code": 401,
        "msg": "请输入Device-Code"
    }

*错误(无设备或无专题)时返回*

    {
        "code": 401,
        "msg": "设备未配置"
    }

*正确时返回*

    {
        "code": 200,
        "data": {
            "id": 10, //专题id
            "theme_id": 1, //样式id
            "title": "测试专题88"  //专题名称
        },
        "msg": ""
    }    

> 设备新增专题    

`(POST) /api/client/device/projects`

*参数*

    device_code  // 设备码
    project_id  // 专题id
    
*错误(未传device_code或project_id)时返回*

    {
        "code": 401,
        "msg": "请输入参数:device_code"
    }
    
*专题不存在时*
    
    {
        "code": 404,
        "msg": "数据不存在"
    }

*返回*

    {
        "code": 200,
        "data": {
            "created_at": "2018-11-05 12:22:20",
            "device_code": "1",
            "id": 8,
            "project_id": 10,
            "updated_at": "2018-11-07 12:31:19"
        },
        "msg": ""
    }    
    
> 设备修改专题    

`(PUT) /api/client/device/projects/<int:project_id>`

*错误(未传Device-Code)时返回*

    {
        "code": 401,
        "msg": "请输入Device-Code"
    }

*错误(无设备或无专题)时返回*

    {
        "code": 401,
        "msg": "设备未配置"
    }     

*返回*    
    
    {
        "code": 200,
        "data": {
            "created_at": "2018-11-05 12:22:20",
            "device_code": "1",
            "id": 8,
            "project_id": 14,
            "updated_at": "2018-11-07 12:25:49"
        },
        "msg": ""
    }
  