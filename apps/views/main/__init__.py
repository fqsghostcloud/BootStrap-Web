from flask import Blueprint

main = Blueprint('main', __name__)  # add Flask-Blueprint


from . import views, forms, error