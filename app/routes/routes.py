from flask import render_template, Blueprint
from flask_login import login_user, logout_user
from models.database import db_session

routes = Blueprint('routes', __name__)
@routes.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('login.html')