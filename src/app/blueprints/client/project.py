from flask import g, request
from . import client_blueprint as api
from plugin.exceptions import ApiError
from app import db
from app.decorators.request_decorators import setting_required, json_args_required
from app.service.utils import api_success
from app.models.statistic_log import StatisticLog
from app.models import Device, Project, ProjectBook, ProjectPicture, ProjectVideo, Book, Video


@api.route('/projects', methods=['GET'])
def get_project():
    # 获取专题列表
    projects = Project.query.\
        with_entities(Project.title,
            Project.id).\
        all()
    res = [p._asdict() for p in projects]
    return api_success(res)


@api.route('/device/project_books', methods=['GET'])
@setting_required
def get_project_books():
    # 获取专题图书
    project_id = g.current_device.project_id
    res = ProjectBook.get_project_books_with_paginate(project_id)
    return api_success(res)


@api.route('/device/project_magazines', methods=['GET'])
@setting_required
def get_project_magazines():
    # 获取专题期刊
    project_id = g.current_device.project_id
    res = ProjectBook.get_project_magazines_with_paginate(project_id)
    return api_success(res)


@api.route('/device/project_papers', methods=['GET'])
@setting_required
def get_project_papers():
    # 获取专题报纸
    project_id = g.current_device.project_id
    res = ProjectBook.get_project_papers_with_paginate(project_id)
    return api_success(res)


@api.route('/device/project_videos', methods=['GET'])
@setting_required
def get_project_videos():
    # 获取专题视频
    project_id = g.current_device.project_id
    res = ProjectVideo.get_project_videos_with_paginate(project_id)
    return api_success(res)


@api.route('/device/project_images', methods=['GET'])
@setting_required
def get_device_project_image():
    # 获取专题图片
    project_id = g.current_device.project_id
    res = ProjectPicture.get_project_image_with_paginate(project_id)
    return api_success(res)


@api.route('/device/project_banners', methods=['GET'])
@setting_required
def get_device_project_banner():
    # 获取专题轮播图
    project_id = g.current_device.project_id
    res = ProjectPicture.get_project_banner_with_paginate(project_id)
    return api_success(res)


@api.route('/device/projects', methods=['GET'])
@setting_required
def get_device_project():
    # 获取当前设备所选专题
    project_id = g.current_device.project_id
    project = Project.query.\
        with_entities(Project.title, Project.theme_id,
            Project.id).\
        filter_by(id=project_id).\
        first_or_404()
    res = project._asdict()
    res['title_first'] = res['title'][:2]
    res['title_second'] = res['title'][2:]
    return api_success(res)


@api.route('/device/projects', methods=['POST'])
@json_args_required('device_code', 'project_id')
def device_save_project():
    # 设备新增专题
    device_code = request.json.get('device_code')
    project_id = request.json.get('project_id')
    Project.query.get_or_404(project_id)
    device = Device.query.filter_by(device_code=device_code).first()
    if not device:
        device = Device(
            device_code=device_code,
            project_id=project_id
        )
    if device.project_id == 0:
        device.project_id = project_id
    device.save()
    return api_success(device.to_dict())


@api.route('/device/projects/<int:project_id>', methods=['PUT'])
@setting_required
def device_change_project(project_id):
    # 设备修改专题
    device = g.current_device
    device.project_id = project_id
    device.save()
    return api_success(device.to_dict())


@api.route('/books/read/<int:book_id>', methods=['GET'])
@setting_required
def read_book(book_id):
    query = Book.query.with_entities(Book.id).\
        filter_by(id=book_id)
    book = query.first()
    if not book:
        raise ApiError('书本不存在')
    query.update({'read_count': Book.read_count + 1})
    db.session.commit()
    books = Book.query.with_entities(Book.id, ProjectBook.project_id).\
        join(ProjectBook, Book.id==ProjectBook.book_id).\
        filter(Book.id==book_id).all()
    StatisticLog.add_read_book_record(books)
    return api_success(books)


@api.route('/videos/play/<int:video_id>', methods=['GET'])
@setting_required
def play_video(video_id):
    query = Video.query.with_entities(Video.id).\
        filter_by(id=video_id)
    video = query.first()
    if not video:
        raise ApiError('视频不存在')
    query.update({'play_count': Video.play_count + 1})
    db.session.commit()
    query = Video.query.with_entities(Video.id, ProjectVideo.project_id).\
        join(ProjectVideo, Video.id==ProjectVideo.video_id).\
        filter(Video.id==video_id)
    videos = query.all()
    StatisticLog.add_play_count_record(videos)
    return api_success(videos)