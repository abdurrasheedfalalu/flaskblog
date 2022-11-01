from flask import Blueprint, render_template, flash, redirect, url_for
from app.forms import LoginForm


auth = Blueprint('auth', __name__, url_prefix="/auth")


@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login succesfully.', 'success')
        return redirect(url_for('home'))
    print(form.errors)
    return render_template('login.html', form=form, title='Login', legend='Login')