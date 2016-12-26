# coding=utf-8
import traceback
from . import db
from flask import current_app
from flask.ext.login import UserMixin, LoginManager
# from apps.views.common.views import session 导入报错


''' from werkzeug.security import generate_password_hash, check_password_hash  ***密码hash加密***'''


login_manager = LoginManager()

class User(db.Model, UserMixin):
    id = db.Column(db.String(50), primary_key=True, nullable=False)
    username = db.Column(db.Unicode(128), nullable=False, unique=True, index=True)
    realname = db.Column(db.Unicode(128))
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50))
    sex = db.Column(db.Unicode(10))

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User %s>' % (self.username)

    '''@property  # what it is meaning?'''



    def save(self):
        db.session.add(self)
        db.session.commit()


    def remove(self):
        db.session.delete(self)
        db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(str(user_id))

def get_by_id(id):
    return User.query.filter(User.id == id).first()

def get_by_username(username):
    return User.query.filter(User.username == username).first()

def get_count():
    return User.query.count()

def check_password(password):
    if User.query.filter(User.password == password).first() is not None:
        return True


'''create user function'''
def create_user(user_form):
    try:
        has_user = get_by_username(user_form.username.data)
        if has_user:
            current_app.logger.warning(u'该用户 %s 已经存在', has_user.username)
            return 'REPRAT'
        user = User(user_form.username.data)
        user.password = user_form.password.data
        user.realname = user_form.realname.data
        user.email = user_form.e_mail.data
        user.sex = user_form.sex.data
        user.id = create_user_id()
        user.save()
        current_app.logger.info(u'添加 %s 用户成功', user.username)
        return 'OK'
    except Exception, e:
        current_app.logger.error(u'添加 %s 用户失败', user_form.username.data)
        current_app.logger.error(traceback.format_exc())
        return 'FAIL'


def create_user_id():
    import time
    localtime = time.localtime(time.time())
    count = 5
    string = ''
    for a in range(count):
        index = count - a
        string = string + str(localtime[index])
    return string

