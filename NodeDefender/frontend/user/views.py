@app.route('/user/profile')
@login_required
def UserProfile():
    Profile = UserModel.query.filter_by(email = current_user.email).first()
    Team =  UserModel.query.all()
    return render_template('user/profile.html', Team = Team, Profile = Profile)

@app.route('/user/inbox')
@login_required
def UserInbox():
    return render_template('user/inbox.html')

@app.route('/user/inbox/<mailid>', methods=['GET', 'POST'])
@login_required
def UserInboxID(mailid):
    message = MessageModel.query.filter_by(uuid=mailid).first()
    return render_template('user/inboxid.html', mailid=mailid, message =
                           message)

@app.route('/user/settings')
@login_required
def UserSettings():
    return render_template('user/settings.html')


