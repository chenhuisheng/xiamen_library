from flask import request
from . import admin_blueprint as api
from app.service.search import Search
from app.service.decorators import admin_login_required, json_args_required
from plugin.exceptions import ApiError
from app.service.utils import api_success, video_allow_extensions
from app.models.video import Video
from app.service import video as video_service
import os


@api.route('/videos', methods=['GET'])
@admin_login_required
def video_export():
    project_id = request.args.get('project_id')
    query = video_service.get_video_query(project_id)
    res = Search().init_query(query).load(Video).paginate()
    res['items'] = video_service.bindTitles(res.get('items', []))
    for item in res['items']:
        item['file_size'] = round(item['file_size'] / 1024 / 1024, 2)
    return api_success(res)

@api.route('/videos/<int:video_id>', methods=['GET'])
@admin_login_required
def get_video(video_id):
    video = Video.get_one(video_id)
    project = video_service.get_video_project(video_id)
    res = video.to_dict()
    res['file_size'] = round(res['file_size'] / 1024 / 1024, 2)
    res['projects'] = project
    return api_success(res)

@api.route('/videos', methods=['POST'])
@json_args_required('title', 'file_path')
@admin_login_required
def add_video():
    data = request.json
    data['file_type'] = os.path.splitext(data['file_path'])[1].strip('.')
    if data['file_type'] not in video_allow_extensions:
        raise ApiError('视频格式不正确')
    data['file_size'] = video_service.get_size(data['file_path'])
    video = Video.create(data)
    res = video.to_dict()
    project_ids = data.get('project_ids', [])
    video_service.generate_project(res['id'], project_ids)
    return api_success(res)

@api.route('/videos2', methods=['POST'])
@json_args_required('video_info')
@admin_login_required
def add_videos():
    datas = request.json.get('video_info', [])
    video_service.batch_add_videos(datas)
    return api_success({})

@api.route('/videos/<int:video_id>', methods=['PUT'])
@admin_login_required
@json_args_required('title')
def update_video(video_id):
    video = Video.query.get(video_id)
    if not video:
        raise ApiError('视频不存在')
    data = request.json
    data['file_size'] = video.file_size
    video = video.update(data)
    res = video.to_dict()
    project_ids = data.get('project_ids',[])
    video_service.generate_project(video_id, project_ids)
    return api_success(res)

@api.route('/videos/<int:video_id>', methods=['DELETE'])
@admin_login_required
def delete_video(video_id):
    video = Video.query.get(video_id)
    if not video:
        raise ApiError('视频不存在')
    video.soft_delete()
    return api_success({})