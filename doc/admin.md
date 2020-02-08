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

#### HOST

`dev.xiamen.chaoxingbook.com`

#### 账号管理

> 新增账号

`(POST) /api/admin/account`

*参数*

    {
        "phone": "13763812350",
        "name": "测试管理员4",
        "password": "123456"
    }

> 编辑账号

`(PUT) /api/admin/account/<int:admin_id>`

*参数*

    {
        "phone": "13763812350",
        "name": "测试管理员4"
    }

> 删除账号

`(DELETE) /api/admin/account/<int:admin_id>`

> 获取管理账号列表

`(GET) /api/admin/account`

> 重置密码

`(POST) /api/admin/account/password_reset`

*参数*

    {
        "admin_id": 1
    }

> 修改密码

`(POST) /api/admin/account/change_password/<int:admin_id>`

*参数*

    {
        "old_password": "123456",
        "new_password": "654321",
        "check_new_password": "654321"
    }

#### 登录与登出

> 登录

`(POST) /api/admin/account/login`

*参数*

    {
        "phone": "13763812345",
        "password": "123456"
    }

> 获取当前登录用户

`(GET) /api/admin/account/current`

*返回*

    {
        "code": 200,
        "data": {
            "created_at": "2018-11-03 10:39:41",
            "creater_id": 0,
            "id": 1,
            "is_delete": false,
            "name": "测试管理员1",
            "phone": "18558707091",
            "updated_at": "2018-11-05 17:52:47"
        },
        "msg": ""
    }

>登出

`(GET) /api/admin/account/logout`

#### 专题管理

> 获取专题列表

`(GET) /api/admin/projects`

*返回*

    {
        "code": 200,
        "data": [
            {
                "book_count": 5,
                "created_at": "2018-11-05 15:55:35",
                "creater_id": 1,
                "id": 10,
                "picture_count": 0,
                "picture_sort": [],
                "summary": "dddddddddddddddddddddd",
                "title": "测试专题8",
                "updated_at": "2018-11-05 21:31:09"
            }
        ],
        "msg": ""
    }

> 新增专题

`(POST) /api/admin/projects`

*参数*

    {
        "title": "测试专题8",
        "summary": "dddddddddddddddddddddd"
    }
    
*返回*

    {
        "code": 200,
        "data": {
            "created_at": "2018-11-03 16:44:23",
            "creater_id": 1,
            "id": 8,
            "picture_sort": [],
            "summary": "dddddddddddddddddddddd",
            "title": "测试专题8",
            "updated_at": "2018-11-03 16:44:23"
        },
        "msg": ""
    }    

> 编辑专题

`(PUT) /api/admin/projects/<int:project_id>`

*参数*

    {
        "title": "测试专题7",
        "summary": "dddddddddddddddddddddd"
    }
    
*返回*

    {
    "code": 200,
    "data": {
        "created_at": "2018-11-03 16:13:52",
        "creater_id": 1,
        "id": 7,
        "picture_sort": [],
        "summary": "dddddddddddddddddddddd",
        "title": "测试专题7",
        "updated_at": "2018-11-03 16:15:15"
    },
    "msg": ""
}    

#### 内容管理

> 获取专题图书列表

`(GET) /api/admin/projects/<int:project_id>/books`

*返回*

    {
        "code": 200,
        "data": [
            {
                "author": ["张培培主编"],
                "catalog": "",
                "catalog_json": [],
                "created_at": "2018-11-03 15:50:30",
                "file_path": "/mnt/g/xiamen_library/src/app/resource/uploads/books/20181103/1541231392.17313481.pdf",
                "file_size": 0,
                "file_type": "pdf",
                "id": 9,
                "image": "/mnt/g/xiamen_library/src/app/resource/uploads/images/20181103/1541230176.797511.jpg",
                "is_delete": false,
                "isbn": "",
                "pages": 0,
                "pub_date": "1970-01-01",
                "publisher": "",
                "summary": "",
                "title": "我不哭",
                "updated_at": "2018-11-03 15:50:30"
            }
        ],
        "msg": ""
    }

> 专题添加图书

`(POST) /api/admin/projects/<int:project_id>/books`

*参数*

    {
        "books": [
            {"book_id":5},
            {"book_id":7},
            {"book_id":9},
            {"book_id":11}
        ]
    }

*返回*

    {
        "code": 200,
        "data": {
            "books": [
                {
                    "book_id": 5,
                    "created_at": "2018-11-03 16:10:32",
                    "id": 18,
                    "project_id": 1,
                    "updated_at": "2018-11-03 16:10:32"
                },
                {
                    "book_id": 7,
                    "created_at": "2018-11-03 16:10:32",
                    "id": 19,
                    "project_id": 1,
                    "updated_at": "2018-11-03 16:10:32"
                },
                {
                    "book_id": 9,
                    "created_at": "2018-11-03 16:10:32",
                    "id": 20,
                    "project_id": 1,
                    "updated_at": "2018-11-03 16:10:32"
                },
                {
                    "book_id": 11,
                    "created_at": "2018-11-03 16:24:18",
                    "id": 21,
                    "project_id": 1,
                    "updated_at": "2018-11-03 16:24:18"
                }
            ],
            "created_at": "2018-11-03 11:36:32",
            "creater_id": 1,
            "id": 1,
            "picture_sort": [
                2,
                1,
                3
            ],
            "summary": "专题介绍专题介绍专题介绍专题介绍",
            "title": "历史记忆",
            "updated_at": "2018-11-03 15:38:32"
        },
        "msg": ""
    }

> 专题删除图书

`(DELETE) /api/admin/projects/<int:project_id>/books/<int:book_id>`

#### 专题轮播图片

> 获取专题轮播图

`(GET) /api/admin/projects/<int:project_id>/loop_picture`

> 轮播图排序

`(POST) /api/admin/projects/<int:project_id>/loop_picture/set_order`

*参数*

    {
        "sorted_ids": [2,1,3]
    }

> 专题添加轮播图

`(POST) /api/admin/projects/<int:project_id>/loop_picture`

*参数*

    {
        "picture_ids": [2,3,4,5]
    }

> 专题删除轮播图

`(DELETE) /api/admin/projects/<int:project_id>/loop_picture/<int:picture_id>`

#### 图书相关

>图书文件上传

`(POST) /api/admin/ebook`

*参数*

    file

*返回*

    {
        "code": 200,
        "data": {
            "file": "/mnt/g/xiamen_library/src/app/resource/uploads/books/20181103/1541231392.17313481.pdf",
            "metadata": ""
        },
        "msg": ""
    }

>图片文件上传

`(POST) /api/admin/image`

*参数*

    file

*返回*

    {
        "code": 200,
        "data": {
            "url": "/mnt/g/xiamen_library/src/app/resource/uploads/images/20181103/1541232667.82893161.jpg"
        },
        "msg": ""
    }

>上传图书

`(POST) /api/admin/books`

*参数*

    {
        "title": "我不哭", //图书标题(必传)
        "file_path": "/mnt/g/xiamen_library/src/app/resource/uploads/books/20181103/1541231392.17313481.pdf",  // 图书文件(必传)
        "image": "/mnt/g/xiamen_library/src/app/resource/uploads/images/20181103/1541230176.797511.jpg",  //图书封面图片(必传)
        "pub_date": "1970-01-01", //出版日期
        "author": "作者1/作者2", //作者与作者之间用“/”隔开
        "isbn": "isbn",
        "publisher": "出版社",
        "pages": 15, //页数
        "catalog": "目录",
        "summary": "摘要",
        "project_ids": [11,34,12] //专题id
    }

*返回*

    {
        "code": 200,
        "data": {
            "author": "作者1/作者2",
            "catalog": "目录",
            "catalog_json": [],
            "created_at": "2018-11-03 16:26:56",
            "file_path": "/mnt/g/xiamen_library/src/app/resource/uploads/books/20181103/1541231392.17313481.pdf",
            "file_size": 0,
            "file_type": "pdf",
            "id": 23,
            "image": "/mnt/g/xiamen_library/src/app/resource/uploads/images/20181103/1541230176.797511.jpg",
            "is_delete": false,
            "isbn": "isbn",
            "pages": 15,
            "pub_date": "1970-01-01",
            "publisher": "出版社",
            "summary": "摘要",
            "title": "我不哭",
            "updated_at": "2018-11-03 16:26:56"
        },
        "msg": ""
    }

>图书查询

`(GET) /api/admin/books`

*参数*

    title_like //图书标题
    author_like //作者

*返回*

    {
        "code": 200,
        "data": {
            "items": {
                "author": "作者1/作者2",
                "catalog": "目录",
                "catalog_json": [],
                "created_at": "2018-11-12 10:57:41",
                "file_path": "/resource/uploads/books/20181112/1541991389.5305314vbird-linux-server-3e.pdf",
                "file_size": 17946242,
                "file_type": "pdf",
                "id": 73,
                "image": "/resource/uploads/images/20181112/1541991432.3267727u8891206113801177793fm27gp0.jpg",
                "is_delete": false,
                "isbn": "isbn",
                "pages": 15,
                "pub_date": "1970-01-01",
                "publisher": "出版社",
                "summary": "摘要",
                "title": "我不哭",
                "projects": [
                    {
                        "id": 10,
                        "name": "测试专题88"
                    },
                    {
                        "id": 11,
                        "name": "a"
                    },
                    {
                        "id": 12,
                        "name": "b"
                    }
                ],
                "updated_at": "2018-11-12 10:57:41"
            },
            "pageIndex": 0,
            "pageSize": 20,
            "totalCount": 1,
            "totalPage": 1
        },
        "msg": ""
    }

>单本图书查询

`(GET) /api/admin/books/<int:book_id>`

*返回*

    {
        "code": 200,
        "data": {
            "author": "作者",
            "catalog": "目录",
            "catalog_json": [],
            "created_at": "2018-11-06 11:19:38",
            "file_path": "/mnt/g/xiamen_library/src/app/resource/uploads/books/20181103/1541231392.17313481.pdf",
            "file_size": 0,
            "file_type": "pdf",
            "id": 34,
            "image": "/mnt/g/xiamen_library/src/app/resource/uploads/images/20181103/1541230176.797511.jpg",
            "is_delete": false,
            "isbn": "isbn",
            "pages": 15,
            "projects": [
                {
                    "id": 10,
                    "title": "测试专题88"
                },
                {
                    "id": 11,
                    "title": "a"
                }
            ],
            "pub_date": "1970-01-01",
            "publisher": "出版社",
            "summary": "摘要",
            "title": "我不哭",
            "updated_at": "2018-11-06 11:19:38"
        },
        "msg": ""
    }

>编辑图书

`(PUT) /api/admin/books/<int:id_>`

*参数*

    {
        "title": "我不哭", //图书标题(必传)
        "file_path": "/mnt/g/xiamen_library/src/app/resource/uploads/books/20181103/1541231392.17313481.pdf",  // 图书文件(必传)
        "image": "/mnt/g/xiamen_library/src/app/resource/uploads/images/20181103/1541230176.797511.jpg",  //图书封面图片(必传)
        "pub_date": "1970-01-01", //出版日期
        "author": "作者1/作者2", //作者与作者之间用“/”隔开
        "isbn": "isbn",
        "publisher": "出版社",
        "pages": 15, //页数
        "catalog": "目录",
        "summary": "摘要",
        "project_ids": [11,34,12] //专题id
    }

*返回*

    {
        "code": 200,
        "data": {
            "author": "",
            "catalog": "",
            "catalog_json": [],
            "created_at": "2018-11-03 15:44:17",
            "file_path": "/mnt/g/xiamen_library/src/app/resource/uploads/images/20181103/1541230286.66042111.pdf",
            "file_size": 0,
            "file_type": "epub",
            "id": 7,
            "image": "/mnt/g/xiamen_library/src/app/resource/uploads/images/20181103/1541230176.797511.jpg",
            "is_delete": false,
            "isbn": "1234567",
            "pages": 0,
            "pub_date": "1970-01-01",
            "publisher": "",
            "summary": "",
            "title": "我不笑",
            "updated_at": "2018-11-03 17:18:29"
        },
        "msg": ""
    }

>删除图书

`(DELETE) /api/admin/books/<int:id_>`

*返回*

    {
        "code": 200,
        "data": {},
        "msg": ""
    }

#### 轮播图片

>获取轮播图片

`(GET) /api/admin/pictures`

*返回*

    {
        "code": 200,
        "data": {
            "items": [
                {
                    "created_at": "2018-11-03 17:35:11",
                    "id": 6,
                    "is_delete": false,
                    "summary": "123456",
                    "title": "11111",
                    "updated_at": "2018-11-03 17:35:11",
                    "url": "/mnt/g/xiamen_library/src/app/resource/uploads/images/20181103/1541230176.797511.jpg"
                },
                {
                    "created_at": "2018-11-03 17:32:16",
                    "id": 5,
                    "is_delete": false,
                    "summary": "",
                    "title": "",
                    "updated_at": "2018-11-03 17:32:16",
                    "url": "/mnt/g/xiamen_library/src/app/resource/uploads/images/20181103/1541230176.797511.jpg"
                },
                {
                    "created_at": "2018-11-03 17:31:38",
                    "id": 4,
                    "is_delete": false,
                    "summary": "",
                    "title": "",
                    "updated_at": "2018-11-03 17:31:38",
                    "url": "/mnt/g/xiamen_library/src/app/resource/uploads/images/20181103/1541230176.797511.jpg"
                },
                {
                    "created_at": "2018-11-03 15:25:09",
                    "id": 3,
                    "is_delete": false,
                    "summary": "test3",
                    "title": "test3",
                    "updated_at": "2018-11-03 15:25:09",
                    "url": ""
                },
                {
                    "created_at": "2018-11-03 15:20:29",
                    "id": 2,
                    "is_delete": false,
                    "summary": "test2",
                    "title": "test2",
                    "updated_at": "2018-11-03 15:20:29",
                    "url": ""
                }
            ],
            "pageIndex": 0,
            "pageSize": 9,
            "totalCount": 5,
            "totalPage": 1
        },
        "msg": ""
    }

>获取单张轮播图片信息

`(GET) /api/admin/pictures/<int:picture_id>`

*返回*

    {
        "code": 200,
        "data": {
            "created_at": "2018-11-06 12:40:00",
            "id": 13,
            "is_delete": false,
            "projects": [],
            "summary": "123456",
            "title": "11111",
            "updated_at": "2018-11-06 12:40:00",
            "url": "/mnt/g/xiamen_library/src/app/resource/uploads/images/20181103/1541230176.797511.jpg"
        },
        "msg": ""
    }

>上传轮播图片

`(POST) /api/admin/pictures`

*参数*

    {
        "url":"/mnt/g/xiamen_library/src/app/resource/uploads/images/20181103/1541230176.797511.jpg",//图片
        "title": "11111",  //图书标题
        "summary": "123456",  //说明
        "project_ids": [11,12,155] //专题id
    }

*返回*

    {
        "code": 200,
        "data": {
            "created_at": "2018-11-03 17:35:11",
            "id": 6,
            "summary": "123456",
            "title": "11111",
            "updated_at": "2018-11-03 17:35:11",
            "url": "/mnt/g/xiamen_library/src/app/resource/uploads/images/20181103/1541230176.797511.jpg"
        },
        "msg": ""
    }

>修改轮播图片

`(PUT) /api/admin/pictures/<int:picture_id>`

*参数*

    {
        "url":"/mnt/g/xiamen_library/src/app/resource/uploads/images/20181103/1541230176.797511.jpg",//图片
        "title": "11111",  //图书标题
        "summary": "123456",  //说明
        "project_ids": [11,12,155] //专题id
    }

*返回*

    {
        "code": 200,
        "data": {
            "created_at": "2018-11-03 17:35:11",
            "id": 6,
            "summary": "123456",
            "title": "11111",
            "updated_at": "2018-11-03 17:35:11",
            "url": "/mnt/g/xiamen_library/src/app/resource/uploads/images/20181103/1541230176.797511.jpg"
        },
        "msg": ""
    }

>删除轮播图片

`(DELETE) /api/admin/pictures/<int:picture_id>`

*返回*

    {
        "code": 200,
        "data": {},
        "msg": ""
    }

