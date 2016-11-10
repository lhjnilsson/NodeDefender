@LoginMan.user_loader
def load_user(id):      # Needed for Flask-login to work.
    return UserModel.query.get(int(id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # If Method is GET is should display login-page
    if request.method == 'GET':
        lform = LoginForm()
        rform = RegisterForm()
        return render_template('login.html', lform = lform, rform = rform)

    lform = LoginForm(request.form)
    # login-stuff to verify if user is correct
    if lform.validate():
        user = UserModel.query.filter_by(email = lform.email.data).first()
        if user is None:
            flash('User or password is invalid', 'error')
            return redirect(url_for('login'))
        if not user.verify_password(lform.password.data, request.remote_addr):
            loginlog = LoginLogModel(False, request.remote_addr,
                                    request.user_agent)
            user.loginlog.append(loginlog)
            db.session.add(user)
            db.session.commit()
            flash('User or password is invalid', 'error')
            return redirect(url_for('login'))
        loginlog = LoginLogModel(True, request.remote_addr,
                                request.user_agent)
        user.loginlog.append(loginlog)
        user.last_login = datetime.now()
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=lform.remember_me())
        return redirect(url_for('index'))
    else:
        flash("Please fill in correctly", "error")
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
def register():
    rform = RegisterForm(request.form)
    if rform.validate():
        UserQuery = UserModel.query.filter_by(email =\
                                              rform.email.data).first()
        if UserQuery is not None:
            flash('Email is already present', 'error')
            return redirect(url_for('login'))
        user = UserModel(rform.firstname.data.capitalize(),
                rform.lastname.data.capitalize(), rform.email.data, \
                rform.password.data)
        WelcomeMessage = MessageModel(subject="Welcome {}!".format(user.firstname), \
                              body=WelcomeText.format(user.firstname))
        # Adds initial Mail to mailbox, welcoming new user.
        user.messages.append(WelcomeMessage)
        db.session.add(user)
        db.session.commit()
        flash('user successfully added', 'success')
        return redirect(url_for('login'))
    else:
        flash('something went wrong in form', 'error')
        return redirect(url_for('login'))

