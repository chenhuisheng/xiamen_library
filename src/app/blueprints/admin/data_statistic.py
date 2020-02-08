from flask import request
from . import admin_blueprint as api
from app.service.utils import api_success
from app.service.decorators import admin_login_required
from app.service import data_statistic


@api.route('/data_statistic', methods=['GET'])
@admin_login_required
def data_statistic_detail():
    date_begin = request.args.get('date_begin')
    date_end = request.args.get('date_end')
    res = data_statistic.statistic_all(date_begin, date_end)
    return api_success(res)