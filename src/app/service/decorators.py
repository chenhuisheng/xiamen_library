from functools import wraps
from datetime import date, datetime
from flask import request, g, current_app
from app.service.utils import api_success
from app.models import Device
from plugin.exceptions import ApiError, UnauthorizedError


def args_required(*req_args):
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            for arg in req_args:
                if not arg in request.args.keys():
                    raise ApiError('请输入参数:{}'.format(arg))
            return func(*args, **kwargs)
        return decorated_view
    return decorator

def json_args_required(*req_args):
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            for arg in req_args:
                if not arg in request.json.keys():
                    raise ApiError('请输入参数:{}'.format(arg))
            return func(*args, **kwargs)
        return decorated_view
    return decorator

def header_required(*header_args):
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            for arg in header_args:
                if not arg in request.headers:
                    raise ApiError('请输入heder:{}'.format(arg))
            return func(*args, **kwargs)
        return decorated_view
    return decorator

def run_times(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        start = datetime.now()
        res = func(*args, **kwargs)
        end = datetime.now()
        delta = end - start
        current_app.logger.info(delta.total_seconds())
        return res
    return decorated_view

def admin_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not g.admin:
            raise UnauthorizedError('请登录')
        return func(*args, **kwargs)
    return decorated_view
