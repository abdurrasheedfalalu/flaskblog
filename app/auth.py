from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import LoginManager, current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app.forms import LoginForm, RegistrationForm
from app.models import User, db


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'danger'

auth = Blueprint('auth', __name__, url_prefix="/auth")


@login_manager.user_loader
def load_user(id):
    user = User.query.get_or_404(int(id))
    return user

@auth.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('blog.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.generate_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form, title='Register', legend='Register')


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            if user.check_password_hash(form.password.data):
                login_user(user, remember=form.remember.data)
                flash('Login succesfully.', 'success')
                next = request.args.get('next')
                if not next or url_parse(next).netloc != '':
                    next = url_for('blog.posts')
                return redirect(next)
        flash('Invalid email or password! try again.', 'danger')
    return render_template('auth/login.html', form=form, title='Login', legend='Login')


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('auth.login'))