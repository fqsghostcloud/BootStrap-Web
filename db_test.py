from flask import Flask
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from apps.models import User
from apps import config
from flask.ext.script import Shell

app = Flask(__name__)
app.config.from_object(config.databaseconfig['videodata'])
db = SQLAlchemy(app)


manager = Manager(app)
''' add shell command enviroment var '''
def make_shell_context():
    return dict(app=app, db=db, User=User.User)

manager.add_command("shell", Shell(make_context=make_shell_context))

manager.run()

