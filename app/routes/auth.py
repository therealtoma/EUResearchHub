from flask import Blueprint, request, render_template, url_for, redirect, flash, current_app
from sqlalchemy import text
from flask_wtf.csrf import CSRFProtect
from app.models.database import db, Researchers, Evaluators
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required, current_user
from app.utils.utils import check_email
from shutil import copy
import os

auth = Blueprint('auth', __name__)


# login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email') # email from the form
        password = request.form.get('password') # password from the form

        usertype = request.form.get('usertype') # type of user that whants to login

        evaluator = Evaluators.query.filter_by(email=email).first()
        researcher = Researchers.query.filter_by(email=email).first()

        if evaluator and check_password_hash(evaluator.password, password):
            login_user(evaluator)
            db.session.close()
            current_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('EVALUATOR_DATABASE_URI')
            return redirect(url_for('views.projects', user_type='evaluator'))
        elif researcher and check_password_hash(researcher.password, password):
            login_user(researcher)
            db.session.close()
            current_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('RESEARCHER_DATABASE_URI')
            return redirect(url_for('views.projects', user_type='researcher'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html')


# register route
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        choice = request.form.get('choice')
        if choice:
            if choice == 'Researcher':
                return render_template('register.html', user='researcher')
            else:
                return render_template('register.html', user='Evaluator')

        name = request.form.get('name') # name from the form
        surname = request.form.get('surname') # surname from the form
        email = request.form.get('email') # email from the form
        password = request.form.get('password') # password from the form
        affiliation = request.form.get('affiliation') # affiliation from the form
        
        # if the affiliation is not set, the user is an evaluator, otherwise a researcher
        # also check if email is already registerd on other table, error in case
        if affiliation is None:
            user = Evaluators.query.filter_by(email=email).first()
            user_other = Researchers.query.filter_by(email=email).first()
        else:
            user = Researchers.query.filter_by(email=email).first()
            user_other = Evaluators.query.filter_by(email=email).first()
            
        if user or user_other:
            flash('Email already registered', category='error')
        elif not check_email(email):
            flash('Email format not valid', category='error')
        elif len(password) < 7:
            flash('Password must be 8 characters', category='error')
        else:

            profile_picture = request.files.get('profile_picture')
            print(profile_picture)
            if profile_picture and profile_picture.filename != '':
                current_directory = os.path.dirname(os.path.realpath(__file__))
                current_app.config['UPLOAD_FOLDER'] = os.path.join(current_directory, '../uploads/profile_images')
                filename = f'{email}.jpg'
                profile_picture.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            else:
                filename = 'default.jpg'

            if affiliation is None:
                new_user = Evaluators(name=name, surname=surname, email=email,
                                      password=generate_password_hash(password, method='sha256'), profile_picture=filename)
            else:
                new_user = Researchers(name=name, surname=surname, email=email,
                                       password=generate_password_hash(password, method='sha256'),
                                       affiliation=affiliation, profile_picture=filename)

            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))
        if affiliation is None:
            return render_template('register.html', user='evaluator')
        else:
            return render_template('register.html', user='researcher')
    return render_template('register.html', user='none')


# logout route
@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('auth.login'))
