from .. import AuthView
from ...models.manage import user as UserSQL
from flask_login import login_user, logout_user
from .forms import LoginForm, RegisterForm, PasswordForm
from flask import request, redirect, url_for, render_template, flash
from datetime import datetime
from ... import serializer
from ...mail import user as UserMail

@AuthView.route('/login', methods=['GET', 'POST'])
def Login():
    login_form = LoginForm(request.form)
    if request.method == 'GET':
        return render_template('auth/login.html', LoginForm = login_form)
    
    if login_form.validate_on_submit():
        user = UserSQL.Get(login_form.email.data)
        if user is None:
            flash('Email or Password Wrong', 'error')
            return render_template('auth/login.html', LoginForm = login_form)
       
        if not user.verify_password(login_form.password.data):
            flash('Email or Password Wrong', 'error')
            return render_template('auth/login.html', LoginForm = login_form)
 
        if not user.active:
            flash('Account Locked', 'error')
            return render_template('auth/login.html', LoginForm = login_form)

        if login_form.remember():
            login_user(user, remember = True)
        else:
            login_user(user)
        
        return redirect(url_for('index'))
    else:
        print(login_form.errors)
        flash('error', 'error')
        return redirect(url_for('AuthView.Login'))

@AuthView.route('/logout')
def Logout():
    logout_user()
    return redirect(url_for('AuthView.Login'))

@AuthView.route('/register/<token>', methods=['GET', 'POST'])
def Register(token):
    user = UserSQL.Get(serializer.loads_salted(token))
    if user is None:
        flash('Invalid Token', 'error')
        return redirect(url_for('index'))

    register_form = RegisterForm()
    if request.method == 'GET':
        return render_template('auth/register.html', RegisterForm =
                               register_form, user = user)
    if register_form.validate_on_submit():
        user.firstname = register_form.firstname.data
        user.lastname = register_form.lastname.data
        user.active = True
        user.confirmed_at = datetime.now()
        UserSQL.Save(user)
        UserSQL.Password(user.email, register_form.password.data)
        UserMail.confirm_user.delay(user.email)
        flash('Register Successful, please login', 'success')
    else:
        print(register_form.errors)
        flash('Error doing register, please try again', 'error')
        return redirect(url_for('AuthView.Login'))
    
    return redirect(url_for('AuthView.Login'))

@AuthView.route('/resetpassword/<token>', methods=['GET', 'POST'])
def ResetPassword(token):
    user = UserSQL.Get(serializer.loads_salted(token))
    if user is None:
        flash('Invalid token', 'error')
        return redirect(url_for('AuthView.Login'))

    password_form = PasswordForm()
    if request.method == 'GET':
        return render_template('auth/reset_password.html', user = user, password_form =
                               password_form)

    if password_form.validate_on_submit():
        UserSQL.Password(user.email, password_form.password)
        UserSQL.Enable(user.email)
    else:
        flash('Error doing register, please try again', 'error')
        return redirect(url_for('AuthView.Login'))
    
    return redirect(url_for('AuthView.Login'))
