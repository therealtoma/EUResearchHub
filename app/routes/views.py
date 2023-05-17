from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models.database import db, Researchers

views  = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('projects.html')