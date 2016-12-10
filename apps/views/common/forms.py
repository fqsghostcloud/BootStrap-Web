# coding=utf8
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, RadioField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(Form):
    username = StringField(u'用户名:', validators=[DataRequired()])
    password = PasswordField(u'密码:', validators=[DataRequired()])
    remember_me = BooleanField(u'记住我', default= False)
    login = SubmitField(u'登录')



class RegisterForm(Form):
    username = StringField(u'用户名:', validators=[DataRequired(), Length(min=4, max=12)])
    password = PasswordField(u'密码:', validators=[DataRequired(), Length(min=6, max=12), EqualTo('password2', message=u'密码必须相同')])
    password2 = PasswordField(u'确认密码:')
    realname = StringField(u'真实姓名:')
    e_mail = StringField(u'您的邮箱:')
    sex = RadioField(u'性别:', choices=[('man', u'男'), ('woman', u'女')], default='man')
    regis_submit = SubmitField(u'注册')




