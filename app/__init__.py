<<<<<<< HEAD
from flask import Flask
=======
from flask import Flask, render_template, redirect, url_for
from flask_wtf.csrf import CSRFError

'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from flask_login import LoginManager
from dotenv import load_dotenv
from routes.routes import routes
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    
    app.register_blueprint(routes)
    
    login_manger = LoginManager()
    login_manger.login_view = 'routes.login'
    
    @app.errorhandler(403)
    def handle_unauthorized(e):
        with app.app_context():
            return render_template('403.html'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        with app.app_context():
            return render_template('404.html'), 404

    return app
    
def create_database(uri):
    engine = create_engine(uri)
    Session = sessionmaker(bind=engine)
    return Session()
    
    
    
'''
# REFACTORING CODE
from flask import Flask, flash
>>>>>>> origin/15-connection_DB
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
from app.models.database import db
import os
<<<<<<< HEAD

load_dotenv()  # loads enviroment variables form .env file

=======
from flask_wtf import CSRFProtect
load_dotenv() # loads enviroment variables form .env file
>>>>>>> origin/15-connection_DB

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
<<<<<<< HEAD
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../uploads/profile_images')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
=======
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DEFAULT_DATABASE_URI')
    csrf = CSRFProtect(app)
    csrf.init_app(app)
>>>>>>> origin/15-connection_DB
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

<<<<<<< HEAD
    return app
=======
    @app.errorhandler(403)
    def handle_unauthorized(e):
        with app.app_context():
            return render_template('403.html'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        with app.app_context():
            return render_template('404.html'), 404

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        flash('CSRF token validation failed', 'error')
        return redirect(url_for('auth.login'))

    return app


>>>>>>> origin/15-connection_DB
