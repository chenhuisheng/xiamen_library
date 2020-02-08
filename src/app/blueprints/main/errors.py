from flask import jsonify
from plugin.exceptions import ApiError, ForbiddenError, ServerError, UnauthorizedError, NotFoundError
from . import main


@main.app_errorhandler(404)
def page_no_found(e):
    response = jsonify({'msg': '数据不存在', 'code': 404})
    response.status_code = 404
    return response

@main.app_errorhandler(500)
def internal_server_error(e):
    response = jsonify({'msg': '服务器开小差了', 'code': 500})
    response.status_code = 500
    return response

@main.app_errorhandler(ApiError)
def api_error(e):
    response = jsonify({'msg': str(e), 'code': 400})
    response.status_code = 400
    return response

@main.app_errorhandler(ForbiddenError)
def forbidden_error(e):
    response = jsonify({'msg': str(e), 'code': 403})
    response.status_code = 403
    return response

@main.app_errorhandler(ServerError)
def server_error(e):
    response = jsonify({'msg': str(e), 'code': 500})
    response.status_code = 500
    return response

@main.app_errorhandler(UnauthorizedError)
def unauthorized_error(e):
    response = jsonify({'msg': str(e), 'code': 401})
    response.status_code = 401
    return response

@main.app_errorhandler(NotFoundError)
def notfound_error(e):
    msg = str(e) or '数据不存在'
    response = jsonify({'msg': msg, 'code': 404})
    response.status_code = 404
    return response
