'''
Copyright (c) 2016 Connection Technology Systems Northern Europe

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE
SOFTWARE.
'''
from . import app, LoginMan, db, icpe, chconf, mqtt, statistics
from flask import render_template, request, flash, redirect, url_for, abort, \
json
from flask_login import login_required, login_user, current_user, logout_user
from .models import UserModel, iCPEModel, NodeModel, MessageModel, LoginLogModel,\
NodeEventModel, NodeHeatStatModel, NodePowerStatModel, NodeNotesModel,\
        NodeNoteStickyModel, NodeClassModel, NodeHiddenFieldModel
from .forms import NodeForm, LoginForm, RegisterForm, AdminServerForm, \
        iCPEConfigForm, NodeBasicForm
from datetime import datetime
from sqlalchemy import desc

# Welcome Text that should be added when new user is added.
WelcomeText = "Welcome to NodeDefender {} \n \
This is currently in rapid development with new features coming out \
every week. Please keep yourself updated on github to stay in touch \
with the new features and report any issues or request features that \
you wish to see. \n \
You can contact me on henrik.nilsson@ctsystem.se \
\n \n \
Best Regards, Henrik"

'''
Login Page for Unauthorized users.
When logged in the achive a cookie that is later used for RESTful API calls
that load data to the webpage
'''
mapcords = chconf.ReadMap()

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


@app.context_processor
def inject_user():      # Adds general data to base-template
    if current_user.is_authenticated:
        # Return Message- inbox for user if authenticated
        messages = UserModel.query.get(current_user.id).messages
        return dict(user = current_user, messages = messages)
    else:
        # If not authenticated user get Guest- ID(That cant be used).
        return dict(user = current_user)

'''
Below is all the pages deliverd to Logged in Users.
All pages are pretty much only sent out without any special data except for a
cookie. Data is later filled in via AJAX from Webpage
'''

@app.route('/')
@app.route('/index')
@login_required
def index():
    nodes = iCPEModel.query.all()
    stats = statistics.GetAllStats()
    nodeevents = NodeEventModel.query.order_by(desc(NodeEventModel.id)).limit(20)
    return render_template('index.html', nodelist=nodes, stats = stats,
                           nodeevents = nodeevents, mapcords = mapcords)

#
# User specific profile-views
#

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

#
# Views for Nodes- view
#

@app.route('/nodes/list', methods=['GET', 'POST'])
@login_required
def NodesList():
    if request.method == 'GET':
        nodes = iCPEModel.query.all()
        return render_template('nodes/list.html', nodes = nodes)
    try:
        icpe.AddiCPE(request.form['mac'], request.form['alias'],
              request.form['street'], request.form['city'])
        flash('Succesfully added node: ' + request.form['mac'], 'success')
        return redirect(url_for('NodesList'))
    except Exception as e:
        flash('Error in adding node: ' + request.form['mac'] + '. ' + str(e), 'danger')
        return redirect(url_for('NodesList'))

@app.route('/nodes/events')
@login_required
def NodesEvents():
    return render_template('nodes/events.html')

@app.route('/nodes/list/<mac>', methods=['GET', 'POST', 'PUT'])
@login_required
def NodesNode(mac):
    iCPE = iCPEModel.query.filter_by(mac = mac).first()
    if not iCPE:
        raise ValueError('Cant find mac')
    form = NodeForm()
    ConfigForm = iCPEConfigForm()
    NodeBasic = NodeBasicForm()
    if request.method == 'GET':
        znodes = icpe.WebForm(mac)
        '''
        powerstat = dict((nodeid, list(events)) for nodeid, events in
                    groupby(iCPE.powerstat, lambda stat: stat.nodeid))
        '''
        return render_template('nodes/node.html', mac=mac, form=form, iCPE =
                               iCPE, znodes = znodes, iCPEConfigForm =
                               ConfigForm, NodeBasicForm = NodeBasic)
    elif request.method == 'POST':
        if ConfigForm.validate_on_submit():
            iCPE.alias = ConfigForm.alias.data
            iCPE.location.street = ConfigForm.street.data
            iCPE.location.city = ConfigForm.city.data
            iCPE.location.geolat = ConfigForm.geolat.data
            iCPE.location.geolong = ConfigForm.geolong.data

        db.session.add(iCPE)
        db.session.commit()
        znodes = icpe.WebForm(mac)
        return render_template('nodes/node.html', mac=mac, form=form, iCPE = iCPE,
                               znodes = znodes,
                          iCPEConfigForm = ConfigForm, NodeBasicForm = NodeBasic)



@app.route('/nodes/list/<mac>/<nodeid>', methods=['GET', 'POST'])
@login_required
def NodesNodeConfigure(mac, nodeid):
    iCPE = iCPEModel.query.filter_by(mac = mac).first()
    if iCPE is None:
        return redirect(url_for('index'))
    NodeBasic = NodeBasicForm()
    if request.method =='POST':
        try:
            ZNode = [node for node in iCPE.znodes if node.nodeid == int(nodeid)][0]
        except IndexError:
            print('could not find ZWave NOde')
            return redirect(url_for('NodesNode', mac=mac))
        icpe.UpdateNodeInfo(**{'Alias' :  NodeBasic.alias.data, 'mac' : mac, 'nodeid' : nodeid})
        ZNode.alias = NodeBasic.alias.data
        db.session.add(ZNode)
        db.session.commit()
        return redirect(url_for('NodesNode', mac=mac))
    return redirect(url_for('NodesNode', mac=mac))

@app.route('/nodes/list/<mac>/<nodeid>/delete')
@login_required
def NodesNodeDelete(mac, nodeid):
    try:
        icpe.DeleteZNode(mac, nodeid)
    except (ValueError, TypeError) as e:
        flash(e, 'danger')
        return redirect(url_for('NodesNode', mac=mac))
   
    flash('Successfully removed node ' + nodeid, 'success')
    return redirect(url_for('NodesNode', mac=mac))

@app.route('/nodes/<mac>/update')
@login_required
def NodesUpdate(mac):
    if not mqtt():
        flash('MQTT is Offline', 'danger')
    else:
        icpe.Event(mac, 'UpdateNode')
        flash('Node ' + mac + ' succesfully updated.', 'success')
    return redirect(url_for('NodesNode',  mac=mac))

@app.route('/nodes/<mac>/include')
@login_required
def NodesInclude(mac):
    if not mqtt():
        flash('MQTT is Offline', 'danger')
    else:
        icpe.Event(mac, 'NodeInclude')
        flash('Node '  + mac + ' in Include for 30sec', 'success')
    return redirect(url_for('NodesNode', mac=mac))

@app.route('/nodes/<mac>/exclude')
@login_required
def NodesExclude(mac):
    if not mqtt():
        flash('MQTT is Offline', 'danger')
    else:
        icpe.Event(mac, 'NodeExclude')
        flash('Node ' + mac + ' in Exclude for 30sec', 'success')
    return redirect(url_for('NodesNode', mac=mac))

@app.route('/nodes/<mac>/notes/add', methods=['GET', 'POST'])
@login_required
def NodesNotesAdd(mac):
    if request.method == 'POST':
        note = request.form['note']
        icpe = iCPEModel.query.filter_by(mac = mac).first()
        dbnote = NodeNotesModel(current_user.email, note)
        icpe.notes.append(dbnote)
        db.session.add(icpe)
        db.session.commit()
        return redirect(url_for('NodesNode', mac=mac))
    else:
        return redirect(url_for('NodesNode', mac=mac))

@app.route('/nodes/<mac>/notes/sticky', methods=['GET', 'POST'])
@login_required
def NodesNoteSticky(mac):
    if request.method == 'POST':
        note = request.form['note']
        icpe = iCPEModel.query.filter_by(mac = mac).first()
        if icpe.notesticky:
            icpe.notesticky.author = current_user.email
            icpe.notesticky.note = note
            icpe.notesticky.created_on = datetime.now()
        else:
            StickyModel = NodeNoteStickyModel(current_user.email, note)
            icpe.notesticky= StickyModel
        db.session.add(icpe)
        db.session.commit()
        return redirect(url_for('NodesNode', mac=mac))
    else:
        return redirect(url_for('NodesNode', mac=mac))

@app.route('/nodes/<mac>/delete')
@login_required
def DeleteNode(mac):
    try:
        icpe.DeleteiCPE(mac)
        flash('Node: ' + mac + ' successfully deleted', 'success')
        return redirect(url_for('NodesList'))
    except Exception as e:
        flash('Unable to remove ' + str(mac) + '. Error: ' + str(e), 'danger')
        return redirect(url_for('NodesList'))


@app.route('/nodes/<mac>/<nodeid>/<cls>/<field>/hide')
def NodesNodeClassHide(mac, nodeid, cls, field):
    if 1 < db.session.query(iCPEModel, NodeModel).\
                            filter(iCPEModel.mac == mac).\
                            filter(NodeModel.nodeid == int(nodeid)).count():
        CleanDuplicate(db.session.query(iCPEModel, NodeModel).\
                                        filter(iCPEModel.mac == mac).\
                                        filter(NodeModel.nodeid == int(nodeid)).all())
    Cls = NodeClassModel.query.join(NodeModel).join(iCPEModel).\
            filter(NodeClassModel.commandclass == cls).\
            filter(NodeModel.nodeid == nodeid).\
            filter(iCPEModel.mac == mac).first()
    Cls.hiddenFields.append(NodeHiddenFieldModel(field))
    db.session.add(Cls)
    db.session.commit()
    icpe.HideNodeClass(mac, nodeid, cls)
    return redirect(url_for('NodesNode', mac=mac))

@app.route('/nodes/<mac>/<nodeid>/<cls>/<field>/display')
def NodesNodeClassDisplay(mac, nodeid, cls, field):
    if 1 < db.session.query(iCPEModel, NodeModel).\
                            filter(iCPEModel.mac == mac).\
                            filter(NodeModel.nodeid == nodeid).count():
        CleanDuplicate(db.session.query(iCPEModel, NodeModel).\
                                        filter(iCPEModel.mac == mac).\
                                        filter(NodeModel.nodeid == nodeid).all())
    Cls = NodeClassModel.query.join(NodeModel).join(iCPEModel).\
            filter(NodeClassModel.commandclass == cls).\
            filter(NodeModel.nodeid == nodeid).\
            filter(iCPEModel.mac == mac).first()
    
    for hiddenfield in Cls.hiddenFields:
        db.session.delete(hiddenfield)
    db.session.commit()
    icpe.DisplayNodeClass(mac, nodeid, cls)
    return redirect(url_for('NodesNode', mac=mac))



def CleanDuplicate(records):
    for icpe, node in records:
        if node.parent_id == None:
            db.session.delete(node)
    db.session.commit()
    return True

#
# Views for Data- view
#

@app.route('/data/power')
def DataPower():
    if request.method == 'GET':
        icpes = iCPEModel.query.all()
        return render_template('data/power.html', icpes = icpes)

@app.route('/data/power/<mac>')
def DataPoweriCPE(mac):
    if request.method == 'GET':
        icpe = iCPEModel.query.filter_by(mac = mac).first()
        return render_template('data/powericpe.html', icpe = icpe)


@app.route('/data/power/<mac>/<nodeid>')
def DataPoweriCPENode(mac, nodeid):
    if request.method == 'GET':
        icpe = iCPEModel.query.filter_by(mac = mac).first()
        return render_template('data/powericpenode.html', icpe = icpe)


@app.route('/data/heat')
def DataHeat():
    if request.method == 'GET':
        icpes = iCPEModel.query.all()
        return render_template('data/heat.html', icpes = icpes)

@app.route('/data/heat/<mac>')
def DataHeatiCPE(mac):
    if request.method == 'GET':
        icpe = iCPEModel.query.filter_by(mac = mac).first()
        return render_template('data/heaticpe.html', icpe = icpe)

@app.route('/data/heat/<mac>/<nodeid>')
def DataHeatiCPENode(mac, nodeid):
    if request.method == 'GET':
        icpe = iCPEModel.query.filter_by(mac = mac).first()
        return render_template('data/heaticpenode.html', icpe = icpe)

@app.route('/data/events')
def DataEvents():
    if request.method == 'GET':
        events = NodeEventModel.query.all()
        return render_template('data/events.html', events = events)

@app.route('/data/events/<mac>')
def DataEventsiCPE(mac):
    if request.method == 'GET':
        events = iCPEModel.query.filter_by(mac = mac).first().events
        return render_template('data/eventsicpe.html', events = events)

@app.route('/data/events/<mac>/<nodeid>')
def DataEventsiCPENode(mac, nodeid):
    if request.method == 'GET':
        icpe = iCPEModel.query.filter_by(mac = mac).first()
        return render_template('data/eventsicpenode.html', icpe = icpe)


#
# Views for Admin- view
#
@app.route('/admin/server')
@login_required
def AdminServer():
    if request.method == 'GET':
        sform = AdminServerForm()
        return render_template('admin/server.html', sform = sform)

@app.route('/admin/sever/setgeneral', methods=['GET', 'POST'])
@login_required
def AdminServerSetGeneral():
    sform = AdminServerForm(request.form)
    if sform.validate():
        flash('Successfully updated General Settings', 'success')
        return redirect(url_for('AdminServer'))
    else:
        flash('Error when trying to update General Settings', 'danger')
        return redirect(url_for('AdminServer'))

@app.route('/admin/users')
@login_required
def AdminUsers():
    return render_template('admin/users.html')

@app.route('/admin/mqtt')
@login_required
def AdminMqtt():
    return render_template('admin/mqtt.html')

@app.route('/admin/backup')
@login_required
def AdminBackup():
    return render_template('admin/backup.html')

'''
error handlers
'''

@app.errorhandler(403) # Trying to access without permission
@login_required
def page_not_allowed(e):
    return render_template('403.html'), 403

@app.errorhandler(404) # Trying to access page that does not exist.
@login_required
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500) # Internal Server Error
@login_required
def internal_server_error(e):
    return render_template('500.html'), 500
