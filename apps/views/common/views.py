# coding=utf8
from apps import app
from flask import render_template, url_for, redirect, request, flash, current_app
from flask.ext.login import login_user, login_required, current_user
from .forms import LoginForm, RegisterForm
from apps.models import User


@app.route('/')
@app.route('/index', methods='GET')
def index():

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(csrf_enabled=False)
    if request.method == 'POST' and form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        password = User.check_password(form.password.data)
        if user is None:
            flash(u'该用户名不存在!')
        elif password is not True:
            flash(u'您的密码错误!')
        else:
            login_user(user, remember=form.remember_me.data)
            return redirect('/view')
    return render_template('login.html', form=form, title=u'欢迎登录')




@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(csrf_enabled=False)
    if request.method == 'POST' and form.validate_on_submit():
        info = User.create_user(form)
        if info == 'OK':
            flash(u'您注册成功!')
            return redirect('/login')
        elif info == 'REPRAT':
            flash(u'您注册的用户名已经存在!')
        elif info == 'FAIL':
            flash(u'您注册失败!')

    return render_template('register.html', form=form, title=u'欢迎注册')



@app.route('/download/<path:filename>')

def download(filename):
    from flask import send_from_directory
    import os.path



    dirpath = os.path.join(app.root_path, 'upload')
    return send_from_directory(dirpath, filename, as_attachment=True)










@login_required
@app.route('/view')
def view():
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
    else:
        return render_template('view.html')

