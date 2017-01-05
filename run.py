#!/usr/bin/env python
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from apps import create_app
from apps.models import db
from apps.models.User import login_manager
from apps.models import User



# Flask app config:
app = create_app('videodata')
manager = Manager(app)  # add Flask-Script
migrate = Migrate(app, db)  # add Flask-Migrate to manage database // user python run db init to create Migrate Database
manager.add_command('db', MigrateCommand)


def make_shell_context():
    return dict(app=app, db=db, User=User.User)


if __name__ == '__main__':
    login_manager.init_app(app)
    manager.add_command("shell", Shell(make_context=make_shell_context)) # add shell env
    manager.run()
