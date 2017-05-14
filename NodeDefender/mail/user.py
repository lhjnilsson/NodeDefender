from .. import LoginMan, app, celery, serializer, mail
from ..models.manage import user as UserSQL
from ..models.SQL import UserModel
from flask_mail import Message
from flask import render_template, url_for


@celery.task
def create_user(user):
    if type(user) == str:
        user = UserSQL.Get(user)

    if user.email == None:
        return False
    msg = Message('Welcome to NodeDefender', sender='noreply@nodedefender.com',
                  recipients=[user.email])
    url = url_for('AuthView.Register',\
                  token = serializer.dumps_salted(user.email))
    msg.body = render_template('mail/user/create_user.txt', user = user, url =
                              url)
    mail.send(msg)
    return True


@celery.task
def confirm_user(user):
    if type(user) == str:
        user = UserSQL.Get(user)

    if user.email == None:
        return False

    msg = Message('Confirm Successful!', sender='noreply@nodedefender.com',
                  recipients=[user.email])
    msg.body = render_template('mail/user/user_confirmed.txt', user = user)
    mail.send(msg)
    return True

@celery.task
def reset_password(user):
    if type(user) == str:
        user = UserSQL.Get(user)

    if user.email == None:
        return False

    msg = Message('Reset password', sender='noreply@nodedefender.com',
                  recipients=[user.email])
    url = url_for('AuthView.ResetPassword',\
                 token = serializer.dumps_salted(user.email))
    msg.body = render_template('mail/user/reset_password.txt', user = user, url =
                              url)
    mail.send(msg)
    return True

@celery.task
def login_changed(user):
    if type(user) == str:
        user = UserSQL.Get(user)
    
    msg = Message('Login changed', sender='noreply@nodedefender.com',
                  recipients=[user.email])
    msg.body = render_template('mail/user/reset_password.txt', user = user)
    mail.send(msg)
    return True
