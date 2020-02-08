from functools import wraps
from flask import request, g
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

def setting_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        device_code = request.headers.get('Device-Code')
        if not device_code:
            raise UnauthorizedError('请输入Device-Code')
        device = Device.get_device(device_code)
        if not device:
            raise UnauthorizedError('设备未配置')
        project_id = device.project_id
        if project_id == 0:
            raise UnauthorizedError('设备未配置')
        g.current_device = device
        return func(*args, **kwargs)
    return decorated_view