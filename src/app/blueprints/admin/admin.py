from flask import request, g
from . import admin_blueprint as api
from plugin.exceptions import ApiError
from app.service.utils import api_success
from app.service.decorators import json_args_required, admin_login_required
from app.service.admin import logout_admin, login
from app.models import Admin


@api.route('/account', methods=['POST'])
@admin_login_required
@json_args_required('phone', 'name')
def admin_create():
    data = request.json
    if 'password' not in data:
        data['password'] = '123456'
    res = Admin.create(data).to_dict()
    return api_success(res)


@api.route('/account/<int:admin_id>', methods=['DELETE'])
@admin_login_required
def admin_soft_delete(admin_id):
    if admin_id == g.admin.id:
        raise ApiError('当前登录用户不可删除')
    return Admin.rest_soft_delete(admin_id)


@api.route('/account/<int:admin_id>', methods=['PUT'])
@admin_login_required
@json_args_required('phone', 'name')
def admin_update(admin_id):
    name = request.json.get('name')
    phone = request.json.get('phone')
    data = {
        'name': name,
        'phone': phone
    }
    admin = Admin.query.get_or_404(admin_id)
    res = admin.update(data)
    return api_success(res.to_dict())


@api.route('/account')
@admin_login_required
def admin_find():
    return Admin.rest_get()


@api.route('/account/password_reset', methods=['POST'])
@admin_login_required
@json_args_required('admin_id')
def reset_password():
    admin_id = request.json.get('admin_id')
    admin = Admin.query.get_or_404(admin_id)
    admin.password = Admin.generate_password('123456')
    admin.save()
    return api_success(msg='密码重置成功')


@api.route('/account/change_password/<int:admin_id>', methods=['POST'])
@admin_login_required
@json_args_required('old_password', 'new_password', 'check_new_password')
def change_password(admin_id):
    old_password = request.json.get('old_password')
    new_password = request.json.get('new_password')
    check_new_password = request.json.get('check_new_password')
    admin = Admin.query.get_or_404(admin_id)
    if not admin.verify_password(old_password):
        raise ApiError('原密码有误')
    if new_password != check_new_password:
        raise ApiError('两次密码不一致')
    admin.password = Admin.generate_password(new_password)
    admin.save()
    return api_success(msg='密码修改成功')


@api.route('/account/login', methods=['POST'])
@json_args_required('phone', 'password')
def admin_login():
    phone = request.json.get('phone')
    password = request.json.get('password')
    admin = login(phone, password)
    return api_success(admin.to_dict())


@api.route('/account/current')
@admin_login_required
def get_current_admin():
    res = g.admin.to_dict()
    return api_success(res)


@api.route('/account/logout')
@admin_login_required
def admin_logout():
    logout_admin()
    return api_success({})
