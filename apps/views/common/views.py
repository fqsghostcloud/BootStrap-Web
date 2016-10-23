# coding=utf8
from apps import app
from flask import render_template, url_for, redirect, request, flash
from flask.ext.login import login_user, login_required
from .forms import LoginForm
from apps.models import User


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = LoginForm(csrf_enabled=False)
    if request.method == 'POST'and form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        password = User.check_password(form.password.data)
        print password
        if user is None:
            flash(u'该用户不存在')
        elif password is not True:
            flash(u'您的密码错误')
        else:
            login_user(user, remember=form.remember_me.data)
            return redirect('/view')
    return render_template('index.html', form=form)





@login_required
@app.route('/view')
def view():
    return render_template('view.html')
