from flask import Flask, render_template
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
    
    
    
