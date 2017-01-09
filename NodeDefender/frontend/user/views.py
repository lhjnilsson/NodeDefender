from .. import UserView
from flask import render_template
from flask_login import login_required, current_user
from .models import UserModel, UserMessageModel

@UserView.route('/user/profile')
@login_required
def UserProfile():
    Profile = UserModel.query.filter_by(email = current_user.email).first()
    Team =  UserModel.query.all()
    return render_template('user/profile.html', Team = Team, Profile = Profile)

@UserView.route('/user/inbox')
@login_required
def UserInbox():
    return render_template('user/inbox.html')

@UserView.route('/user/inbox/<mailid>', methods=['GET', 'POST'])
@login_required
def UserInboxID(mailid):
    message = UserMessageModel.query.filter_by(uuid=mailid).first()
    return render_template('user/inboxid.html', mailid=mailid, message =
                           message)

@UserView.route('/user/settings')
@login_required
def UserSettings():
    return render_template('user/settings.html')


