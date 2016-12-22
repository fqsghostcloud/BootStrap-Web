# coding=utf8
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, RadioField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(Form):
    username = StringField(u'用户名:', validators=[DataRequired(message=u'请输入用户名!')])
    password = PasswordField(u'密码:', validators=[DataRequired(message=u'请输入密码!')])
    remember_me = BooleanField(u'记住我', default= False)
    login = SubmitField(u'登录')



class RegisterForm(Form):
    username = StringField(u'用户名:', validators=[DataRequired(message=u'用户名不能为空!'), Length(min=2, max=6, message=u'用户名长度必须在2-6个字符之间!')])
    password = PasswordField(u'密码:', validators=[DataRequired(message=u'密码不能为空!'), Length(min=6, max=12, message=u'您的密码长度必须在6-12个字符之间!')])
    password2 = PasswordField(u'确认密码:',validators=[EqualTo('password', message=u'两次输入的密码必须相同!')])
    realname = StringField(u'真实姓名:')
    e_mail = StringField(u'您的邮箱:')
    sex = RadioField(u'性别:', choices=[('man', u'男'), ('woman', u'女')], default='man')
    regis_submit = SubmitField(u'注册')




