from flask import render_template
from flask_login import login_required, current_user
from NodeDefender.frontend.views import user_view
import NodeDefender

@user_view.route('/user/profile')
@login_required
def UserProfile():
    Team =  UserModel.query.all()
    return render_template('user/profile.html', Team = Team)

@user_view.route('/user/groups')
@login_required
def UserGroups():
    Team =  UserModel.query.all()
    return render_template('user/groups.html', Team = Team)


@user_view.route('/user/inbox')
@login_required
def UserInbox():
    return render_template('user/inbox.html')

@user_view.route('/user/inbox/<mailid>', methods=['GET', 'POST'])
@login_required
def UserInboxID(mailid):
    message = UserMessageModel.query.filter_by(uuid=mailid).first()
    return render_template('user/inboxid.html', mailid=mailid, message =
                           message)
