from flask_login import login_user, logout_user
from NodeDefender.frontend.forms.auth import LoginForm, RegisterForm, PasswordForm
from flask import request, redirect, url_for, render_template, flash
from datetime import datetime
from NodeDefender import serializer
from NodeDefender.frontend.views import auth_view
import NodeDefender

@auth_view.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if request.method == 'GET':
        return render_template('frontend/auth/login.html', LoginForm = login_form)
    
    if login_form.validate_on_submit():
        user = NodeDefender.db.user.get(login_form.email.data)
        if user is None:
            flash('Email or Password Wrong', 'error')
            return render_template('frontend/auth/login.html', LoginForm = login_form)
       
        if not user.verify_password(login_form.password.data):
            flash('Email or Password Wrong', 'error')
            return render_template('frontend/auth/login.html', LoginForm = login_form)
 
        if not user.enabled:
            flash('Account Locked', 'error')
            return render_template('frontend/auth/login.html', LoginForm = login_form)

        if login_form.remember():
            login_user(user, remember = True)
        else:
            login_user(user)
        
        return redirect(url_for('index'))
    else:
        flash('error', 'error')
        return redirect(url_for('auth_view.login'))

@auth_view.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth_view.login'))

@auth_view.route('/register/<token>', methods=['GET', 'POST'])
def register(token):
    user = NodeDefender.db.user.get(serializer.loads_salted(token))
    if user is None:
        flash('Invalid Token', 'error')
        return redirect(url_for('index'))

    register_form = RegisterForm()
    if request.method == 'GET':
        return render_template('frontend/auth/register.html', RegisterForm =
                               register_form, user = user)
    if register_form.validate_on_submit():
        user.firstname = register_form.firstname.data
        user.lastname = register_form.lastname.data
        user.enabled = True
        user.confirmed_at = datetime.now()
        NodeDefender.db.user.save_sql(user)
        NodeDefender.db.user.set_password(user.email, register_form.password.data)
        NodeDefender.mail.user.confirm_user(user.email)
        flash('Register Successful, please login', 'success')
    else:
        flash('Error doing register, please try again', 'error')
        return redirect(url_for('auth_view.login'))
    
    return redirect(url_for('auth_view.login'))

@auth_view.route('/resetpassword/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = UserSQL.Get(serializer.loads_salted(token))
    if user is None:
        flash('Invalid token', 'error')
        return redirect(url_for('auth_view.login'))

    password_form = PasswordForm()
    if request.method == 'GET':
        return render_template('frontend/auth/reset_password.html', user = user,
                               PasswordForm = password_form)

    if password_form.validate_on_submit():
        NodeDefender.db.user.set_password(user.email, password_form.password.data)
    else:
        flash('Error doing register, please try again', 'error')
        return redirect(url_for('auth_view.login'))
    
    return redirect(url_for('auth_view.login'))
