from .. import AuthView
from ...models.manage import user as UserSQL
from flask_login import login_user
from .forms import LoginForm
from flask import request, redirect, url_for, render_template, flash
from datetime import datetime
from ... import serializer

@AuthView.route('/login', methods=['GET', 'POST'])
def Login():
    login_form = LoginForm()
    if request.method == 'GET':
        return render_template('auth/login.html', LoginForm = login_form)
    
    if login_form.validate_on_submit():
        user = UserSQL.Get(login_form.email.data)
        if user is None:
            flash('Email or Password Wrong', 'error')
            return render_template('auth/login.html', LoginForm = login_form)
        login_user(user, remember = login_form.remember.data)
        return redirect(url_for('index'))

@AuthView.route('/register/<token>', methods=['GET', 'POST'])
def Register(token):
    email = serializer.loads_salted(token)
    if email:
        user = UserSQL.Get(email)
    else:
        flash('Invalid Token', 'error')
        return redirect(url_for('index'))

    if user is None:
        flash('User not found', 'error')
        return redirect(url_for('index'))

    register_form = RegisterForm()
    if request.method == 'GET':
        return render_template('auth/register.html', register_form =
                               RegisterForm, user = user)

    if register_form.validate_on_submit():
        user.firstname = register_form.firstname.data
        user.lastname = register_form.lastname.data
        user.active = True
        user.confirmed_at = datatime.now()
        db.session.add(user)
        db.session.commit()
        UserSQL.Password(user.email, password)
        flash('Register Successful, please login', 'success')
    
    return redirect(url_for('AuthView.Login'))
