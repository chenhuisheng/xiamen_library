from flask import request, g
from plugin.exceptions import ApiError
from . import admin_blueprint as api
from app.service.decorators import admin_login_required, json_args_required
from app.service.utils import api_success
from app.models import Project, ProjectBook, Picture, ProjectPicture, Book
from app.service.project import bind_pictures
from sqlalchemy import func
import copy


@api.route('/projects', methods=['POST'])
@admin_login_required
@json_args_required('title')
def create_project():
    # 创建专题
    title = request.json.get('title')
    project = Project.query.filter_by(title=title).first()
    if project:
        raise ApiError('专题名称不可重复')
    data = {
        'title': title,
        'summary': request.json.get('summary', ''),
        'creater_id': g.admin.id
    }
    res = Project.create(data)
    return api_success(res.to_dict())


@api.route('/projects/<int:project_id>', methods=['PUT'])
@admin_login_required
@json_args_required('title')
def update_project(project_id):
    # 编辑专题
    title = request.json.get('title')
    list_project_id = [project_id]
    project_title = Project.query.filter(~Project.id.in_(list_project_id)).\
        filter_by(title=title).\
        first()
    if project_title:
        raise ApiError('专题名称不可重复')
    project = Project.query.get_or_404(project_id)
    data = {
        'title': title,
        'summary': request.json.get('summary', '')
    }
    res = project.update(data)
    return api_success(res.to_dict())


@api.route('/projects', methods=['GET'])
@admin_login_required
def get_project():
    # 获取专题列表
    projects = Project.query.with_entities(Project.id, Project.title, Project.summary).all()
    project_books = Book.query.\
        join(ProjectBook, Book.id==ProjectBook.book_id). \
        with_entities(ProjectBook.project_id, func.count(ProjectBook.book_id).label('book_count')).\
        filter(Book.book_type=='book').\
        group_by(ProjectBook.project_id).all()
    project_pictures = Picture.query.\
        join(ProjectPicture, Picture.id==ProjectPicture.picture_id). \
        with_entities(ProjectPicture.project_id, func.count(ProjectPicture.picture_id).label('banner_count')).\
        filter(Picture.type=='banner').\
        group_by(ProjectPicture.project_id).all()
    pb_count_dict = {pb.project_id: pb.book_count for pb in project_books}
    pp_count_dict = {pp.project_id: pp.banner_count for pp in project_pictures}
    projects = [p._asdict() for p in projects]
    for project in projects:
        project['book_count'] = pb_count_dict.get(project['id'], 0)
        project['picture_count'] = pp_count_dict.get(project['id'], 0)
    return api_success(projects)


@api.route('/projects/<int:project_id>/books', methods=['GET'])
@admin_login_required
def get_project_books(project_id):
    # 获取专题图书列表
    project = Project.query.get_or_404(project_id)
    books = ProjectBook.get_project_books(project.id)
    return api_success(books)


@api.route('/projects/<int:project_id>/books', methods=['POST'])
@json_args_required('books')
@admin_login_required
def create_project_books(project_id):
    # 专题创建图书
    project = Project.query.get_or_404(project_id)
    books = request.json.get('books', [])
    ProjectBook.generate(project.id, books)
    res = project.get_with_books()
    return api_success(res)


@api.route('/projects/<int:project_id>/books/<int:book_id>', methods=['DELETE'])
@admin_login_required
def delete_project_book(project_id, book_id):
    # 专题删除图书
    ProjectBook.remove_book(project_id, book_id)
    return api_success(msg='专题图书删除成功')


@api.route('/projects/<int:project_id>/loop_picture', methods=['GET'])
@admin_login_required
def get_project_picture(project_id):
    # 获取专题轮播图
    project = Project.query.get_or_404(project_id)
    ids = project.picture_sort
    project_picture = ProjectPicture.query.\
        filter(ProjectPicture.picture_id.in_(ids)).\
        filter_by(project_id=project_id).\
        all()
    picture_ids = [p.picture_id for p in project_picture]
    sort_ids = [i for i in ids if i in picture_ids]
    project.picture_sort = sort_ids
    project.save()
    pictures = Picture.query.filter(Picture.id.in_(picture_ids)).all()
    if len(picture_ids) != 0:
        res = bind_pictures(pictures, sort_ids)
        return api_success(res)
    return api_success([])


@api.route('/projects/<int:project_id>/loop_picture/set_order', methods=['POST'])
@admin_login_required
@json_args_required('sorted_ids')
def picture_set_order(project_id):
    # 专题排序轮播图
    project = Project.query.get_or_404(project_id)
    sorted_ids = request.json.get('sorted_ids', [])
    if len(sorted_ids) == 0:
        raise ApiError('轮播图的id列表不能为空')
    project.picture_sort = sorted_ids
    res = project.picture_sort
    project.save()
    return api_success(res)


@api.route('/projects/<int:project_id>/loop_picture', methods=['POST'])
@admin_login_required
@json_args_required('picture_ids')
def create_project_picture(project_id):
    # 专题添加轮播图
    project = Project.query.get_or_404(project_id)
    picture_ids = request.json.get('picture_ids', [])
    ProjectPicture.generate_project_picture(project_id, picture_ids)
    pictures = Picture.query.\
        filter(Picture.id.in_(picture_ids)).\
        all()
    ids = {p.id: p.id for p in pictures}
    image_ids = []
    for i in picture_ids:
        if ids.get(i):
            image_ids.append(ids.get(i))
    new_picture_sort = copy.deepcopy(project.picture_sort)
    for _id in image_ids:
        if _id in new_picture_sort:
            continue
        new_picture_sort.insert(0, _id)
    project.picture_sort = new_picture_sort
    res = project.get_with_pictures()
    project.save()
    return api_success(res)


@api.route('/projects/<int:project_id>/loop_picture/<int:picture_id>', methods=['DELETE'])
@admin_login_required
def delete_project_picture(project_id, picture_id):
    # 专题删除轮播图
    project = Project.query.get_or_404(project_id)
    picture = Picture.query.get_or_404(picture_id)
    ProjectPicture.remove_picture(project_id, picture_id)
    new_picture_sort = copy.deepcopy(project.picture_sort)
    new_picture_sort.remove(picture.id)
    project.picture_sort = new_picture_sort
    project.save()
    return api_success(msg='专题图书删除成功')