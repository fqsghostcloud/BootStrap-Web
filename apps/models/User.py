# coding=utf-8
import traceback
from . import db
from flask import current_app
from flask.ext.login import UserMixin, LoginManager, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash # generate password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from .Role import Role, Permission

login_manager = LoginManager()

# Flask-Login 默认提供UserMixin类，实现了is_anthenticated(), is_active(), is_anonymous()等方法
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String(50), primary_key=True, nullable=False, unique=True)
    username = db.Column(db.Unicode(128), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(50))
    sex = db.Column(db.Unicode(10))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # confirmed = db.Column(db.Boolean, default=False) # confirm the account is active

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User %s>' % (self.username)


    @property
    def password(self):
        raise AttributeError(u'密码不可读取!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    def save(self):
        db.session.add(self)
        db.session.commit()


    def remove(self):
        db.session.delete(self)
        db.session.commit()


    def get_permissions(self):
        if self.role_id is not None:
            return Role.query.filter(Role.id == self.role_id).first().permissions
        else:
            return False


    def can(self, permissions): #return self.role_id is not None and (self.role_id.permissions & permissions) == permissions
        return (self.get_permissions() & permissions) == permissions

    def is_administer(self):
        return self.can(Permission.ADMINISTER)


'''
    # 使用itsdangerous生成确认令牌
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dump({'confirm_id': self.id})

    # 验证令牌信息
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KRY'])
        try:
            data = s.load(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True
'''





@login_manager.user_loader
def load_user(user_id):
    return User.query.get(str(user_id))

def get_by_id(id):
    return User.query.filter(User.id == id).first()

def get_by_username(username):
    return User.query.filter(User.username == username).first()

def get_count():
    return User.query.count()



# register user function
def create_user(user_form):
    try:
        has_user = get_by_username(user_form.username.data)
        if has_user:
            current_app.logger.warning(u'该用户 %s 已经存在', has_user.username)
            return 'REPRAT'
        user = User(user_form.username.data)
        user.password = user_form.password.data
        user.email = user_form.e_mail.data
        user.sex = user_form.sex.data
        user.id = create_user_id()
        user.role_id = Role.query.filter(Role.default == True).first().id # set role to user
        user.save()
        current_app.logger.info(u'添加 %s 用户成功', user.username)
        return 'OK'
    except Exception, e:
        current_app.logger.error(u'添加 %s 用户失败', user_form.username.data)
        current_app.logger.error(traceback.format_exc())
        return 'FAIL'

# use register time to create user id
def create_user_id():
    import time
    localtime = time.localtime(time.time())
    count = 5
    string = ''
    for a in range(count):
        index = count - a
        string = string + str(localtime[index])
    return string

# if user not login
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administer(self):
        return False

login_manager.anonymous_user = AnonymousUser

