import os
from flask import request, current_app
from . import admin_blueprint as api
from app.service.search import Search
from app.service.decorators import admin_login_required, json_args_required, args_required
from plugin.exceptions import ApiError
from app.service.utils import api_success
from app.models.book import Book
from app.models.project import Project
from app.service import book as book_service


@api.route('/books', methods=['GET'])
@admin_login_required
@args_required('book_type')
def book_export():
    book_type = request.args.get('book_type')
    project_id = request.args.get('project_id')
    query = book_service.get_book_query(book_type, project_id)
    res = Search().init_query(query).load(Book).paginate()
    res['items'] = Project.bindTitles(res.get('items', []))
    return api_success(res)

@api.route('/books/<int:book_id>', methods=['GET'])
@admin_login_required
def get_book(book_id):
    book = Book.get_one(book_id)
    projects = Project.get_book_project(book_id)
    res = book.to_dict()
    res['projects'] = projects
    return api_success(res)

@api.route('/books', methods=['POST'])
@json_args_required('title', 'file_path', 'book_type')
@admin_login_required
def add_book():
    data = request.json
    data['file_type'] = os.path.splitext(data['file_path'])[1].strip('.')
    data['file_size'] = book_service.get_size(data['file_path'])
    if data['file_type'] == 'epub':
        file_path = current_app.config['APP_PATH'] + data['file_path']
        opf_path = book_service.generate_opf_from_epub(file_path, data['file_path'])
        data['opf_path'] = os.path.join((data['file_path'] + "_files/"), opf_path)
    if not data.get('image') and data['file_type'] == 'epub':
        cover_path = book_service.cover_path_from_epub(data['file_path'])
        data['image'] = cover_path
    book = Book.create(data)
    project_ids = data.get('project_ids', [])
    res = book.to_dict()
    Project.generate_project(book.id, project_ids)
    return api_success(res)

@api.route('/books/<int:id_>', methods=['PUT'])
@admin_login_required
@json_args_required('title', 'file_path')
def update_book(id_):
    book = Book.query.get(id_)
    if not book:
        raise ApiError('书本不存在')
    data = request.json
    book = book.update(data)
    book = book.to_dict()
    project_ids = data.get('project_ids', [])
    Project.generate_project(id_, project_ids)
    return api_success(book)

@api.route('/books/<int:id_>', methods=['DELETE'])
@admin_login_required
def delete_book(id_):
    book = Book.query.get(id_)
    if not book:
        raise ApiError('书本不存在')
    book.soft_delete()
    return api_success({})