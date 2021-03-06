# coding=utf8
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, RadioField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp
from apps.models import Role
from apps.models import User

class LoginForm(Form):
    username = StringField(u'用户名:', validators=[DataRequired(message=u'请输入用户名!')])
    password = PasswordField(u'密码:', validators=[DataRequired(message=u'请输入密码!')])
    remember_me = BooleanField(u'记住我', default= False)
    login = SubmitField(u'登录')



class RegisterForm(Form):
    username = StringField(u'用户名:', validators=[DataRequired(message=u'用户名不能为空!'), Length(min=2, max=6, message=u'用户名长度必须在2-6个字符之间!')])
    password = PasswordField(u'密码:', validators=[DataRequired(message=u'密码不能为空!'), Length(min=6, max=12, message=u'您的密码长度必须在6-12个字符之间!')])
    password2 = PasswordField(u'确认密码:',validators=[EqualTo('password', message=u'两次输入的密码必须相同!')])
    email = StringField(u'您的邮箱:')
    sex = RadioField(u'性别:', choices=[(v,v) for v in User.Gender], default=u'男')
    regis_submit = SubmitField(u'注册')


class UserConfigForm(Form):
    username = StringField(u'用户名:', validators=[DataRequired(message=u'用户名不能为空!'), Length(min=2, max=6, message=u'用户名长度必须在2-6个字符之间!')])
    email = StringField(u'您的邮箱:')
    sex = RadioField(u'性别:', choices=[(v,v) for v in User.Gender])
    submit = SubmitField(u'保存')


class EditProfileAdminForm(Form):
    username = StringField(u'用户名:', validators=[DataRequired(message=u'用户名不能为空!'), Length(min=2, max=6, message=u'用户名长度必须在2-6个字符之间!')])
    email = StringField(u'邮箱:')
    sex = RadioField(u'性别:', choices=[(v,v) for v in User.Gender])
    role = RadioField(u'权限:', coerce=int)
    submit = SubmitField(u'保存')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.get_role_name(Role.Role.name)]
        self.user = user

    def validate_username(self, field):
        if field.data != self.user.username and User.get_by_username(field.data):
            raise ValueError(u'该用户名已经被使用!')
        else:
            return True

    def validate_email(self, field):
        if field.data != self.user.email and User.get_by_email(field.data):
            raise ValueError(u'该邮箱已经注册!')
        else:
            return True


class TurnToUserId(Form):
    userid = StringField(u'用户ID:')
    submit = SubmitField(u'编辑用户')

class CommentForm(Form):
    body = TextAreaField(u'发表你的评论:', validators=[DataRequired(message=u'评论不能为空!')])
    submit = SubmitField(u'提交')






