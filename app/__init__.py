from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
from app.models.database import db
import os

load_dotenv()  # loads enviroment variables form .env file


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../uploads/profile_images')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()
    # registro i blueprints
    from .routes.auth import auth
    app.register_blueprint(auth, url_prefix='/')

    from .routes.views import views
    app.register_blueprint(views, url_prefix='/')

    from .models.database import Researchers, Evaluators
    @login_manager.user_loader
    def load_user(id):
        return Evaluators.query.get(int(id))

    return app
