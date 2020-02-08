#coding: utf-8

import json
from flask import current_app, request, g
from app.service.admin import get_admin
from . import admin_blueprint as admin

# 初始化g.user
@admin.before_request
def before_request():
    g.admin = get_admin()