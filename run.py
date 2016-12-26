from flask.ext.script import Manager
from flask.ext.moment import Moment
from apps import create_app
from apps.models import db
from apps.models.User import login_manager
from flask.ext.migrate import Migrate, MigrateCommand


# Flask app config:
app = create_app('videodata')
manager = Manager(app) #add Flask-Script
moment = Moment(app) #add time-moment
migrate = Migrate(app, db) # add Flask-Migrate to manage database // user python BootStrap-Web db init to create Migrate Database
manager.add_command('db', MigrateCommand)



if __name__ == '__main__':
   # app.secret_key = "super secret key"
    login_manager.init_app(app)

    manager.run()
