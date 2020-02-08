import os
from flask import request
from . import admin_blueprint as api
from app.service.decorators import admin_login_required
from plugin.exceptions import ApiError
from app.service.utils import api_success, upload_to_images, upload_to_video, upload_to_videos
from app.service.book import upload_book, parse_epub_info
from app.service import video as video_service

@api.route('/upload/image', methods=['POST'])
@admin_login_required
def upload_attachment():
    file_ = request.files.get('file')
    if not file_:
        raise ApiError('请选择要上传的文件')
    data = upload_to_images(file_)
    if data.get('status') is True:
        res = {
            'url': data.get('url', ''),
        }
        return api_success(res)
    raise ApiError('上传失败')

@api.route('/upload/ebook', methods=['POST'])
@admin_login_required
def upload_ebook():
    file_ = request.files.get('file')
    if not file_:
        raise ApiError('请选择要上传的文件')
    data = upload_book(file_)
    if data.get('status') is True:
        if not os.path.splitext(data['url'])[1]=='.pdf':
            metadata = parse_epub_info(file_)
        else:
            metadata = ''
        res = {
            'file': data.get('url', ''),
            'metadata': metadata,
            'pdf_image': data.get('pdf_image') if data.get('pdf_image') else ''
        }
        return api_success(res)
    raise ApiError('上传失败')

@api.route('/upload/video', methods=['POST'])
@admin_login_required
def upload_video():
    file_ = request.files.get('file')
    if not file_:
        raise ApiError('请选择要上传的文件')
    data = upload_to_video(file_)
    url = data.get('url', '')
    file_size = round(video_service.get_size(url) / 1024 / 1024, 2)
    if data.get('status') is True:
        res = {
            'url': url,
            'thumbnail': data.get('thumbnail', ''),
            'file_size': file_size,
            'file_name': file_.filename
        }
        return api_success(res)
    raise ApiError('上传失败')

@api.route('/upload/videos', methods=['POST'])
@admin_login_required
def upload_videos():
    files = request.files.getlist('file')
    if not files:
        raise ApiError('请选择要上传的文件')
    data = upload_to_videos(files)
    if not data:
        raise ApiError('上传失败')
    return api_success(data)
