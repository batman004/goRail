from flask import Flask, Blueprint
from flask_login import LoginManager
from .config import *
import os

def create_app():
    app = Flask(__name__)

    # app.config.from_object(os.environ['APP_SETTINGS'])
    app.config.from_object(DevelopmentConfig)

    # app.config['DEBUG'] = False
    # # TESTING = False
    # # CSRF_ENABLED = True
    # app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from .extensions import db
    from .views import views
    from .auth import auth

    db.init_app(app)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Passenger,Ticket

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(Passenger_id):
        return Passenger.query.get(int(Passenger_id))

    return app



