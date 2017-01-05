
from datetime import timedelta
import os


class Config:
    '''safe config'''
    SSL_DISABLE = True
    CSRF_ENABLE = True
    SECRET_KEY = 'You never guss'

    '''sql config'''
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    '''session cookie_life_time config ???'''
    PERMANENT_SESSION_LIFETIME = timedelta(days=3)
    REMEMBER_COOKIE_DURATION = timedelta(days=3)

    ''' send email config '''
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT= 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = '1178996513@qq.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    #MAIL_PASSWORD = 'ptrwrmfoewwqhjaj'




'''sql_database_config'''
class VideoDataConfig(Config):
        DEBUG = True
        SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://sa:123456@localhost:1433/VideoData?charset=utf8'


databaseconfig = {

    'videodata': VideoDataConfig

}
