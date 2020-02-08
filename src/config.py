import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    ENV = 'development'
    SECRET_KEY = '0HP1WbrZxq4u1f1f'
    APP_PATH = '{}/app'.format(basedir)
    JSON_AS_ASCII = False
    IMAGE_PATH = '{}/resource/uploads/images/'.format(APP_PATH)
    BOOK_PATH = '{}/resource/uploads/books/'.format(APP_PATH)
    VIDEO_PATH = '{}/resource/uploads/videos/'.format(APP_PATH)
    PER_PAGE = 20

    LOG_LEVEL = logging.INFO

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    #数据库IP地址
    DB_ADDR = 'rm-2zeu17et22d652j3n7o.mysql.rds.aliyuncs.com'
    DB_PORT = 3306
    DB_NAME = 'xiamen_library_dev'
    USER_NAME = 'xiamen_library_dev'
    PASSWORD = '33hvegEuNgfTrgqa'

    SQLALCHEMY_POOL_SIZE = 5
    SQLALCHEMY_MAX_OVERFLOW = 5
    SQLALCHEMY_POOL_TIMEOUT = 3600
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{username}:{password}@{db_addr}:{db_port}/{db_name}'.\
        format(username=USER_NAME, password=PASSWORD, db_addr=DB_ADDR, db_name=DB_NAME, db_port=DB_PORT)

class ProductionConfig(Config):
    ENV = 'production'
    SECRET_KEY = 'q5mUrGRLt7lMlbqz'
    #数据库IP地址
    DB_ADDR = os.environ.get('XIAMEN_DB_ADDR', '')
    DB_PORT = os.environ.get('XIAMEN_DB_PORT', 3306)
    DB_NAME = os.environ.get('XIAMEN_DB_NAME', '')
    USER_NAME = os.environ.get('XIAMEN_DB_USER_NAME', '')
    PASSWORD = os.environ.get('XIAMEN_DB_PASSWORD', '')

    SQLALCHEMY_POOL_SIZE = 60
    SQLALCHEMY_MAX_OVERFLOW = 40
    SQLALCHEMY_POOL_TIMEOUT = 3600
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{username}:{password}@{db_addr}:{db_port}/{db_name}'.\
        format(username=USER_NAME, password=PASSWORD, db_addr=DB_ADDR, db_name=DB_NAME, db_port=DB_PORT)

config = {
    'development' : DevelopmentConfig,
    'production' : ProductionConfig,
    'default' : DevelopmentConfig,
}