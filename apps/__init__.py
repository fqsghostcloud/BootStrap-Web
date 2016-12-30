from flask import Flask
from flask.ext.moment import Moment
from config import databaseconfig
from apps.models import User
from apps.models import db
from apps.views.main import main as main_blueprint


app = Flask(__name__)
moment = Moment()  # add Time-Moment
app.config['SECRET_KEY'] = 'You never guss'


def create_app(config):
    app.config.from_object(databaseconfig[config])
    app.register_blueprint(main_blueprint) # register main_blueprint
    db.init_app(app)
    moment.init_app(app)


    return app



from . import views
