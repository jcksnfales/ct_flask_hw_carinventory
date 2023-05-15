from forms import UserLoginForm, UserRegisterForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserRegisterForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            existing_users = [e[0] for e in db.session.query(User.email).all()]
            if email in existing_users:
                flash(f'"{email}" has already been registered.', category='auth-register-failed')
                return redirect(url_for('auth.signup'))
            else:
                user = User(email, password = password)
                db.session.add(user)
                db.session.commit()

                flash(f'Successfully registered "{email}"', category='auth-register-success')
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid form data: Please check your form')
    return render_template('sign_up.html', form=form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()
    
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('Successfully logged in.', 'auth-login-success')
                return redirect(url_for('site.profile'))
            else:
                flash('Login failed.', category='auth-login-failed')
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid Form Data: Please Check your Form')
    return render_template('sign_in.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    flash('Successfully logged out.', 'auth-logout-success')
    return redirect(url_for('auth.signin'))