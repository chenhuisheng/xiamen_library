#coding: utf-8

from flask import session, g
from plugin.exceptions import ApiError
from app.models import Admin


def get_admin():
    admin_id = session.get('admin_id')
    if not admin_id:
        return None
    admin = Admin.query.get(admin_id)
    if not admin:
        admin = None
        logout_admin()
    return admin

def login_admin(admin):
    session['admin_id'] = admin.id
    g.admin = admin
    return True

def logout_admin():
    session.pop('admin_id')

def login(phone, password):
    phone = phone.strip()
    admin = Admin.query.\
        filter_by(phone=phone).\
        filter_by(is_delete=False).\
        first()
    if not admin:
        raise ApiError('该手机未注册')
    if admin.verify_password(password):
        login_admin(admin)
        return admin
    raise ApiError('密码错误')