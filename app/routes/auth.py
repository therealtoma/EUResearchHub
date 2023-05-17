from flask import Blueprint, request, render_template, url_for, redirect, flash
from app.models.database import db, Researchers, Evaluators
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app.modules.modules import check_email

auth = Blueprint('auth', __name__)

# login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('emai') # email from the form
        password = request.form.get('password') # password from the form
        
        usertype = request.form.get('usertype') # type of user that whants to login
        print(usertype)
        
    return render_template('login.html')

# register route
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        choice = request.form.get('choice')
        if choice:
            if choice == 'researcher':
                return render_template('register.html', user='researcher')
            else:
                return render_template('register.html', user='evaluator')
        
        name = request.form.get('name') # name from the form
        surname = request.form.get('surname') # surname from the form
        email = request.form.get('email') # email from the form
        password = request.form.get('password') # password from the form
        affiliation = request.form.get('affiliation') # affiliation from the form
        
        # if the affiliation is not set, the user is an evaluator
        if affiliation is None:
            user = Evaluators.query.filter_by(email=email).first() # find user from database
        else:
            user = Researchers.query.filter_by(email=email).first() # find user from databse
            
        if user:
            flash('Email already registered', category='error')
        elif not check_email(email):
            flash('Email format not valid', category='error')
        elif len(password) < 7:
            flash('Password must be 8 characters', category='error')
        else:
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
    '''
    if request.method == 'POST':
        choice = request.form.get('user') # type of user to create
        if choice == 'researcher':
            return render_template('register.html', user='researcher')
        elif choice == 'evaluator':
            return render_template('register.html', user='evaluator')
        else:
            name = request.form.get('name') # name from the form
            surname = request.form.get('surname') # surname from the form
            email = request.form.get('email') # email from the form
            password = request.form.get('password') # password from the form
            profile_picture = request.form.get('profile_picture') # profile picture from the form
            affiliation = request.form.get('affiliation') # affiliation from the form
                
    return render_template('register.html', user='none')
    '''

# logout route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))