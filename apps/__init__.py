from flask import Flask
from config import databaseconfig
from apps.models import User
from apps.models import db


app = Flask(__name__)


def create_app(config):
    app.config.from_object(databaseconfig[config])
    db.init_app(app)


    return app



from . import views
