from .. import LoginMan, app, celery, serializer
from ..models.manage import user as UserSQL
from ..models.SQL import UserModel
from itsdangerous import URLSafeTimedSerializer

@celery.task
def create_user(user):
    try:
        user = UserSQL.Create(email)
    except ValueError:
        return
    token = serializer.dumps_salted(email)
    url = url_for('AuthView.Register', token=token)
    template = render_template('auth/register.txt', url=url, user = user)
    subject = 'Welcome to NodeDefender'
    send_email(user.email, subject, template)
    return True

@celery_task
def confirm_user(user):
    pass

@celery_task
def login_user(user, request):
    pass

@celery_task
def reset_password(user):
    pass
