from flask import request
from . import admin_blueprint as api
from app.service.search import Search
from app.service.decorators import admin_login_required, json_args_required, args_required
from plugin.exceptions import ApiError
from app.service.utils import api_success
from app.models.picture import Picture
from app.service import picture as picture_service
from app.models.project_picture import ProjectPicture
from app.models.project import Project
from sqlalchemy import and_


@api.route('/pictures', methods=['GET'])
@admin_login_required
@args_required('type')
def picture_export():
    type_ = request.args.get('type')
    project_id = request.args.get('project_id')
    query = picture_service.get_picture_query(project_id, type_)
    res = Search().init_query(query).load(Picture).paginate()
    res['items'] = picture_service.bindTitles(res.get('items', []))
    return api_success(res)

@api.route('/pictures/<int:picture_id>', methods=['GET'])
@admin_login_required
def get_picture(picture_id):
    picture = Picture.get_one(picture_id)
    project = Project.get_picture_project(picture_id)
    res = picture.to_dict()
    res['projects'] = project
    return api_success(res)

@api.route('/pictures', methods=['POST'])
@json_args_required('url', 'type')
@admin_login_required
def add_picture():
    data = request.json
    picture = Picture.create(data)
    res = picture.to_dict()
    project_ids = data.get('project_ids', [])
    picture_service.generate_project(project_ids, res['id'])
    return api_success(res)

@api.route('/pictures/<int:picture_id>', methods=['PUT'])
@admin_login_required
@json_args_required('url')
def update_picture(picture_id):
    picture = Picture.query.get(picture_id)
    if not picture:
        raise ApiError('图片不存在')
    data = request.json
    picture = picture.update(data)
    res = picture.to_dict()
    project_ids = data.get('project_ids', [])
    picture_service.generate_project(project_ids, picture_id)
    return api_success(res)

@api.route('/pictures/<int:picture_id>', methods=['DELETE'])
@admin_login_required
def delete_picture(picture_id):
    picture = Picture.query.get(picture_id)
    if not picture:
        raise ApiError('图片不存在')
    picture.soft_delete()
    return api_success({})