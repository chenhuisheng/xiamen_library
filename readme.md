# 部署文档



## 目录规划

    /var/www/kindle    # 项目主目录
    /var/www/kindle/web    # 后端根目录
    /var/www/kindle/logs   # 日志目录


## 后端

> 项目地址

    
> 依赖

- python v3.4
- virtualenv (python虚拟环境)

> python 安装

    > sudo yum install python34
    > sudo yum install python34-pip
    > sudo yum install python34-devel

> virtualenv 安装

    > sudo yum install virtualenv

> 项目部署

    # 进入项目目录<project_path>
    > cd /var/www/kindle/web
    # 安装python虚拟环境
    > virtualenv -p /usr/bin/python34 ./venv
    # 激活虚拟环境
    > source ./venv/bin/active
    # 升级setuptools和pip
    > pip3 install -U setuptools -i https://pypi.douban.com/simple
    > pip3 install -U pip -i https://pypi.douban.com/simple
    # 安装依赖
    > pip3 install -r ./requirement.txt -i https://pypi.douban.com/simple
    # 启动项目, 项目启动后运行在5000端口
    > ./venv/bin/python3 ./runserver production



## 配置文件

> supervisor配置（web 项目）

    [program:bi_web]
    command=/var/www/kindle/web/venv/bin/python3 /var/www/kindle/web/runserver.py production
    directory=/var/www/kindle/web
    stdout_logfile/var/www/kindle/logs/app.log
    numprocs=1
    autostart=true
    autorestart=true
    redirect_stderr=true
    stopsignal=KILL
    user=root

> supervisor配置（远程打标签任务目）

    # 注意线上需配置环境变量：MIKE_BI_CONFIG=production
    [program:tag_remote_consumer]
    command=/var/www/kindle/web/venv/bin/python /var/www/kindle/web/manage.py member_tag_remote
    directory=/var/www/kindle/web
    stdout_logfile=/var/www/kindle/logs/member_tag_remote.log
    numprocs=1
    autostart=true
    autorestart=true
    redirect_stderr=true
    stopsignal=KILL
    user=root

> supervisor配置（本地打标签任务目）

    # 注意线上需配置环境变量：MIKE_BI_CONFIG=production
    [program:tag_local_consumer]
    command=/var/www/kindle/web/venv/bin/python /var/www/kindle/web/manage.py member_tag_local
    directory=/var/www/kindle/web
    stdout_logfile=/var/www/kindle/logs/member_tag_local.log
    numprocs=1
    autostart=true
    autorestart=true
    redirect_stderr=true
    stopsignal=KILL
    user=root

> nginx配置

    upstream mike_data_server {
        server 127.0.0.1:5001;
        keepalive 64;
    }

    server {
        listen       80;
        server_name         report.chidaoni.com;
        access_log   /var/www/kindle/logs/nginx.access.log;
        error_log    /var/www/kindle/logs/nginx.error.log;
        root  /var/www/kindle/static/dist;

        add_header Strict-Transport-Security max-age=63072000;
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;

        location ~* \.(js|css|png|jpg|jpeg|gif|ico|swf|pdf|mov|fla|zip|rar)$ {
            log_not_found off;
            access_log off;
        }

        location = /robots.txt {
            log_not_found off;
            access_log off;
        }

        location = /favicon.ico {
            log_not_found off;
            access_log off;
        }

        location ~^/service {
            proxy_pass                          http://mike_data_server;
            proxy_http_version                  1.1;
            proxy_set_header  Connection        "";
            proxy_set_header  Host              $host;
            proxy_set_header  X-Forwarded-For   $proxy_add_x_forwarded_for;
            proxy_set_header  X-Real-IP         $remote_addr;
        }
    }