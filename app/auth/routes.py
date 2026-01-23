# Student ID: 24071105
# Student Name: Riya Adhikari

from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User


auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user:
            flash('Email already registered.', 'danger')
            return redirect(url_for('auth.register'))
            
        if User.create(form.username.data, form.email.data, form.password.data):
             flash('Account created! You can now login.', 'success')
             return redirect(url_for('auth.login'))
        else:
             flash('An error occurred. Please try again.', 'danger')

    return render_template('auth/register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user and User.check_password(form.email.data, form.password.data):
            session['user_id'] = user.user_id
            session['username'] = user.username
            session['role'] = user.role
            flash('Logged in successfully.', 'success')
            
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


