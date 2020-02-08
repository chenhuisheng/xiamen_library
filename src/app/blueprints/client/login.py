from flask import request, g
from . import client_blueprint as api
from plugin.exceptions import ApiError
from app.service.utils import api_success
from app.service.decorators import json_args_required, admin_login_required
from app.service.admin import logout_admin, login
from app.models import Admin


@api.route('/login', methods=['POST'])
@json_args_required('phone', 'password')
def admin_login():
    phone = request.json.get('phone')
    password = request.json.get('password')
    admin = Admin.query.filter_by(phone=phone).first()
    if not admin:
        raise ApiError('用户不存在')
    if not admin.verify_password(password):
        raise ApiError('密码错误')
    return api_success(admin.to_dict())