# coding=utf8
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, RadioField
from wtforms.validators import DataRequired

class LoginForm(Form):
    username = StringField(u'用户名:', validators=[DataRequired()])
    password = PasswordField(u'密码:', validators=[DataRequired()])
    remember_me = BooleanField(u'记住我', default= False)



class RegisterForm(Form):
    username = StringField(u'用户名:', validators=[DataRequired()])
    password = PasswordField(u'密码:', validators=[DataRequired()])
    realname = StringField(u'真实姓名:')
    e_mail = StringField(u'您的邮箱:')
    sex = RadioField(u'性别:', choices=[('man', u'男'), ('woman', u'女')])

