# coding: utf-8

import os, time, json, hashlib, math, random, string, calendar, binascii, subprocess
import cv2
import tempfile
from pdf2image import convert_from_path
from hashlib import md5
from decimal import Decimal
from werkzeug import secure_filename
from flask import current_app, request, g
from flask_sqlalchemy import BaseQuery
from datetime import datetime, timedelta, date


def allowed_file(filename, allow_extensions):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in allow_extensions

default_extensions = set(['png', 'jpg', 'jpeg', 'gif',
    'PNG', 'JPG', 'JPEG', 'GIF', 'pdf', 'PDF', 'doc', 'DOC', 'docx', 'DOCX'])

video_allow_extensions = ['mp4', 'flv', 'f4v', 'm4v', 'mpg', 'mpeg', 'mkv', 'avi',
                          'rm', 'rmvb', 'wmv', 'mov', 'MP4', 'FLV', 'MKV', 'AVI',
                          'RM', 'RMVB', 'WMV','MOV', 'F4V', 'M4V', 'MPG', 'MPEG']

def upload(file, thumb=False, allow_extensions=default_extensions):
    sub_folder = datetime.today().strftime('%Y%m%d')
    upload_folder = os.path.join(current_app.static_folder, 'uploads/{}'.format(sub_folder))
    if not os.path.isdir(upload_folder):
        os.mkdir(upload_folder)
    if file and allowed_file(file.filename, allow_extensions):
        original = secure_filename(file.filename)
        if original in default_extensions:
            original = '.' + original
        filename = str(time.time()) + original
        file_static = '/uploads/{}/'.format(sub_folder) + filename
        real_file = os.path.join(upload_folder, filename)
        file.save(real_file)
        res = {
            "status": True,
            "url": file_static,
            "title": original,
            "original": original
        }
        return res
    return {'status': False}


def pagination(query, ignore=None, to_dict=True):
    page = int(request.args.get('pageIndex', 0))
    pageSize = int(request.args.get('pageSize', current_app.config['PER_PAGE']))
    data = query.paginate(page+1, pageSize, error_out=False)
    items = []
    for item in data.items:
        if ignore and isinstance(ignore, list):
            for field in ignore:
                item.__dict__.pop(field)
        if not to_dict:
            items.append(item)
        elif item:
            to_dict_func = 'to_dict'
            if isinstance(to_dict, str):
                to_dict_func = to_dict
            items.append(getattr(item, to_dict_func)())
    res = {
        'items': items,
        'pageIndex': data.page - 1,
        'pageSize': data.per_page,
        'totalCount': data.total,
        'totalPage': data.pages
    }
    return res

def get_today():
    today = datetime.today()
    return date_format(today)

def get_yestoday():
    yestoday = datetime.today()-timedelta(days=1)
    return date_format(yestoday)

def get_days_delta(days):
    '''
        根据距离今天的天数获取日期
    '''
    current_date = datetime.today()+timedelta(days=days)
    return date_format(current_date)

def get_days_delta_by_string(date_str, days):
    '''
        指定日期字符串获取某天日期
    '''
    current_date = datetime.strptime(date_str, '%Y-%m-%d')
    res = current_date + timedelta(days=days)
    return date_format(res)

def get_month_range_by_string(date_str, month_delta=0):
    '''
        根据日期字符串获取当月起止日期
    '''
    current_date = datetime.strptime(date_str, '%Y-%m-%d')
    year = current_date.year
    month = current_date.month + month_delta
    first_day_weekday, month_last_day = calendar.monthrange(year, month)
    month_first_day = date(year=year, month=month, day=1)
    month_last_day = date(year=year, month=month, day=month_last_day)
    return [date_format(month_first_day), date_format(month_last_day)]



def date_format(d):
    return date.strftime(d, '%Y-%m-%d')


def _add_month_interval (dt,inter):
    m=dt.month+inter-1
    y=dt.year+math.floor(m/12)
    m=m % 12 +1
    return (y,m)

def add_month_interval (dt,inter):
    y,m=_add_month_interval(dt,inter)
    y2,m2=_add_month_interval(dt,inter+1)
    maxD=( date(y2,m2,1) - timedelta(days=1) ).day
    d= dt.day<=maxD and dt.day or maxD
    return date(y,m,d)

def add_year_interval (dt,inter):
    return add_month_interval(dt,inter*12)

def random_char(count):
    return ''.join(random.choice(string.ascii_letters) for x in range(count))

def to_json(data):
    for attr in data:
        value = data.get(attr)
        if isinstance(value, datetime):
            value = value.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(value, date):
            value = value.strftime('%Y-%m-%d')
        if isinstance(value, Decimal):
            value = str(value)
        data[attr] = value
    return data

def date_parse(date_str, format='%Y-%m-%d'):
    d = datetime.strptime(date_str, format)
    return d.date()

def date_delta(date_begin, date_end):
    if isinstance(date_begin, str):
        date_begin = date_parse(date_begin)
    if isinstance(date_end, str):
        date_end = date_parse(date_end)
    delta = date_end - date_begin
    return delta.days

def get_today_time():
    today = datetime.today()
    return datetime(today.year, today.month, today.day, 0, 0, 0)

def api_success(data={}, code=200, msg=''):
    return {
        "code": code,
        "data": data,
        'msg': msg
    }

def items_to_dict(items):
    res = [item.to_dict() for item in items]
    return {
        'items': res
    }

def safe_filename(filename):
    for skip in [':', ' ', '<', '>', '/', '\\', '|', '"', '?', '\r', '\n']:
        filename = filename.replace(skip, '_')
    return filename

# Padding for the input string --not
# related to encryption itself.
BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[0:-ord(s[-1])]

def upload_to_images(file_, allow_extensions=default_extensions):
    sub_folder = datetime.today().strftime('%Y%m%d')
    image_path = current_app.config['IMAGE_PATH']
    upload_folder = os.path.join(image_path, sub_folder)
    if not os.path.isdir(upload_folder):
        os.mkdir(upload_folder)
    if file_ and allowed_file(file_.filename, allow_extensions):
        original = secure_filename(file_.filename)
        if original in default_extensions:
            original = '.' + original
        filename = str(time.time()) + original
        images_res = os.path.join(sub_folder, filename)
        url = os.path.join('/resource/uploads/images/', images_res)
        file_.save(os.path.join(image_path, images_res))
        res = {
            "status": True,
            "url": url
        }
        return res
    return {'status': False}

def upload_to_videos(files):
    from app.service import video as video_service
    allow_extensions = ['mp4', 'flv', 'mkv', 'avi' 'rmvb']
    sub_folder = datetime.today().strftime('%Y%m%d')
    video_path = current_app.config['VIDEO_PATH']
    image_path = current_app.config['IMAGE_PATH']
    upload_video_folder = os.path.join(video_path, sub_folder)
    upload_image_folder = os.path.join(image_path, sub_folder)
    if not os.path.isdir(upload_video_folder):
        os.mkdir(upload_video_folder)
    if not os.path.isdir(upload_image_folder):
        os.mkdir(upload_image_folder)
    videos = []
    for file_ in files:
        try:
            if file_ and allowed_file(file_.filename, allow_extensions):
                original = secure_filename(file_.filename)
                if original in default_extensions:
                    original = '.' + original
                filename = str(time.time()) + original
                videos_res = os.path.join(sub_folder, filename)
                url = os.path.join('/resource/uploads/videos/', videos_res)
                file_.save(os.path.join(video_path, videos_res))
                video_input_path = os.path.join(video_path, videos_res)
                image_res = os.path.join(sub_folder, filename.replace(videos_res.split('.')[-1], 'jpg'))
                img_output_path = os.path.join(image_path, image_res)
                get_thumbnail_from_video(video_input_path, img_output_path)
        except Exception as e:
            current_app.logger.error('视频上传失败', e)
            continue
        else:
            thumbnail = os.path.join('/resource/uploads/images/', videos_res.replace(videos_res.split('.')[-1], 'jpg'))
            file_size = round(video_service.get_size(url) / 1024 / 1024, 2)
            res = {
                "url": url,
                "thumbnail": thumbnail,
                'file_size': file_size,
                'file_name': file_.filename
            }
            videos.append(res)
    return videos

def upload_to_video(file_):
    sub_folder = datetime.today().strftime('%Y%m%d')
    video_path = current_app.config['VIDEO_PATH']
    image_path = current_app.config['IMAGE_PATH']
    upload_video_folder = os.path.join(video_path, sub_folder)
    upload_image_folder = os.path.join(image_path, sub_folder)
    if not os.path.isdir(upload_video_folder):
        os.mkdir(upload_video_folder)
    if not os.path.isdir(upload_image_folder):
        os.mkdir(upload_image_folder)
    if file_ and allowed_file(file_.filename, video_allow_extensions):
        original = secure_filename(file_.filename)
        if original in default_extensions:
            original = '.' + original
        filename = str(time.time()) + original
        videos_res = os.path.join(sub_folder, filename)
        url = os.path.join('/resource/uploads/videos/', videos_res)
        file_.save(os.path.join(video_path, videos_res))
        video_input_path = os.path.join(video_path, videos_res)
        image_res = os.path.join(sub_folder, filename.replace(videos_res.split('.')[-1], 'jpg'))
        img_output_path = os.path.join(image_path, image_res)
        get_thumbnail_from_video(video_input_path, img_output_path)
        thumbnail = os.path.join('/resource/uploads/images/', videos_res.replace(videos_res.split('.')[-1], 'jpg'))
        res = {
            "status": True,
            "url": url,
            "thumbnail": thumbnail
        }
        return res
    return {'status': False}

def get_thumbnail_from_video(video_input_path, img_output_path):
    vidcap = cv2.VideoCapture(video_input_path)
    success, image = vidcap.read()
    count = 0
    success = True
    while success:
        # 读取视频帧
        success, image = vidcap.read()
        count += 1
        if count == 150:  # 把第150帧作为封面
            cv2.imwrite(img_output_path, image)  # 保存帧图片
            break

def sort_by_id_list(objects, id_list):
    obj_dict = {}
    for obj in objects:
        if isinstance(obj, dict):
            obj_dict[obj['id']] = obj
        else:
            obj_dict[obj.id] = obj
    res = []
    for id_ in id_list:
        if obj_dict.get(id_):
            res.append(obj_dict.get(id_))
    for id_, obj in obj_dict.items():
        if obj not in res:
            res.append(obj)
    return res

def pdf_to_image(pdf_path, output_image_path):
    with tempfile.TemporaryDirectory() as path:
        # first_page截取开始页, last_page结束页
        images_from_path = convert_from_path(pdf_path, 500, first_page=1, last_page=1)
        for page in images_from_path:
            page.save(output_image_path, 'JPEG')
