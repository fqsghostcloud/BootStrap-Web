from flask.ext.script import Manager
from flask.ext.moment import Moment
from flask.ext.bootstrap import Bootstrap
from apps import create_app
from apps.models.User import login_manager

app = create_app('videodata')
manager = Manager(app)
bootstrap = Bootstrap(app) # test Flask-Bootstrap
moment = Moment(app)


if __name__ == '__main__':
   # app.secret_key = "super secret key"
    login_manager.init_app(app)

    manager.run()
