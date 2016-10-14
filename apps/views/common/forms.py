# coding=utf8
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    username = StringField(u'用户名:', validators=[DataRequired()])
    password = PasswordField(u'密码:', validators=[DataRequired()])
    remember_me = BooleanField(u'记住我', default= False)