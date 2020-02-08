#coding: utf-8

import json
from flask import current_app, request, g
from . import main

# 初始化g.user
@main.before_app_request
def before_request():
    if current_app.config['DEBUG']:
        current_app.logger.info('method: %s' % request.method)
        if hasattr(request, 'args') and dict(request.args):
            current_app.logger.info('args: %s' % json.dumps(dict(request.args)))
        if hasattr(request, 'json') and request.json:
            current_app.logger.info('json: %s' % json.dumps(request.json))        