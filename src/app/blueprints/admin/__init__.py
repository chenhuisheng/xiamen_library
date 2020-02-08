# coding: utf-8

from flask import Blueprint

admin_blueprint = Blueprint('admin', __name__)

from . import base, book, request_decorator, picture, admin, project, video, data_statistic
