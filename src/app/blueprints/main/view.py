from flask import g, current_app
from app import db
from . import main
from plugin.exceptions import ApiError

@main.route('/test')
def test():
    current_app.logger.info('test')
    return 'hello world'


