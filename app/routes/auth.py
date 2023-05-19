<<<<<<< HEAD
from flask import Blueprint, request, render_template, url_for, redirect, flash, current_app
=======
from flask import Blueprint, request, render_template, url_for, redirect, flash
from sqlalchemy import text
from flask_wtf.csrf import CSRFProtect


>>>>>>> origin/15-connection_DB
from app.models.database import db, Researchers, Evaluators
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required, current_user
from app.utils.utils import check_email
<<<<<<< HEAD
from shutil import copy
import os
=======
import os

from flask import current_app
>>>>>>> origin/15-connection_DB

auth = Blueprint('auth', __name__)

# login route
@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email') # email from the form
        password = request.form.get('password') # password from the form
<<<<<<< HEAD
        
        usertype = request.form.get('usertype') # type of user that whants to login
        
=======
        print(email)
        evaluator = Evaluators.query.filter_by(email=email).first()
        researcher = Researchers.query.filter_by(email=email).first()

        if evaluator and check_password_hash(evaluator.password, password):
            login_user(evaluator)
            db.session.close()
            print(os.getenv('EVALUATOR_DATABASE_URI'))
            current_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('EVALUATOR_DATABASE_URI')
            return redirect(url_for('views.projects'))
        elif researcher and check_password_hash(researcher.password, password):
            login_user(researcher)
            db.session.close()
            current_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('RESEARCHER_DATABASE_URI')
            return redirect(url_for('projects'))
        else:
            flash('Invalid email or password', 'error')


>>>>>>> origin/15-connection_DB
    return render_template('login.html')






# register route
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        choice = request.form.get('choice')
<<<<<<< HEAD

        if choice:
            if choice == 'Researcher':
                return render_template('register.html', user='Researcher')
=======
        print(choice)
        if choice:
            if choice == 'Researcher':
                return render_template('register.html', user='researcher')
>>>>>>> origin/15-connection_DB
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
            if profile_picture and profile_picture.filename != '':
                current_directory = os.path.dirname(os.path.realpath(__file__))
                current_app.config['UPLOAD_FOLDER'] = os.path.join(current_directory, '../uploads/profile_images')
                filename = secure_filename(profile_picture.filename)
                profile_picture.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))


            if affiliation is None:
                new_user = Evaluators(name=name, surname=surname, email=email, password=generate_password_hash(password, method='sha256'))
            else:
                new_user = Researchers(name=name, surname=surname, email=email, password=generate_password_hash(password, method='sha256'), affiliation=affiliation)
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