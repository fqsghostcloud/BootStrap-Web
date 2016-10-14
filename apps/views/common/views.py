from apps import app
from flask import render_template, url_for, redirect
from .forms import LoginForm

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = LoginForm(csrf_enabled=False)
    if form.validate_on_submit():
        return redirect('/view')

    return render_template('index.html', form=form)

@app.route('/view')
def view():
    return render_template('view.html')
