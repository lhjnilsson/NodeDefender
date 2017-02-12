from .. import AdminView
from .forms import (GeneralForm, CreateUserForm, CreateGroupForm,
                    CreateMQTTForm, UserSettings, UserPassword, UserGroupAdd)
from flask_login import login_required, current_user
from flask import Blueprint, request, render_template, flash, redirect, url_for
from ...models.manage import user as UserSQL
from ...models.manage import group as GroupSQL
from ...models.manage import mqtt as MQTTSQL
from ...models.SQL import GroupModel, UserModel

@AdminView.route('/admin/server', methods=['GET', 'POST'])
@login_required
def AdminServer():
    General = GeneralForm()
    MQTTList = MQTTSQL.List()
    MQTT = CreateMQTTForm()
    if request.method == 'GET':
        return render_template('admin/server.html', GeneralForm = General,
                               MQTTList = MQTTList, MQTTForm = MQTT)
    if MQTT.Submit.data and MQTT.validate_on_submit():
        try:
            MQTTSQL.Create(MQTT.IPAddr.data,\
                           MQTT.Port.data,\
                           MQTT.Username.data,\
                           MQTT.Password.data)
        except ValueError as e:
            flash('Error: {}'.format(e), 'danger')
            return redirect(url_for('AdminView.AdminServer'))
    
    if General.Submit.data and General.validate_on_submit():
        flash('Successfully updated General Settings', 'success')
        return redirect(url_for('AdminServer'))
    else:
        flash('Error when trying to update General Settings', 'danger')
        return redirect(url_for('AdminView.AdminServer'))

    flash('{}'.format(e), 'success')
    return redirect(url_for('AdminView.AdminServer'))

@AdminView.route('/admin/groups', methods=['GET', 'POST'])
@login_required
def AdminGroups():
    GroupForm = CreateGroupForm()
    groups = GroupSQL.List()
    if request.method == 'GET':
        return render_template('admin/groups.html', groups = groups,
                                CreateGroupForm = GroupForm)
    else:
        if not GroupForm.validate_on_submit():
            flash('Form not valid', 'danger')
            return redirect(url_for('AdminView.AdminGroups'))
        try:
            Group = GroupSQL.Create(GroupForm.Name.data, GroupForm.Description.data)
            Group.email = GroupForm.Email.data
            GroupSQL.Save(Group)
        except ValueError as e:
            flash('Error: {}'.format(e), 'danger')
            return redirect(url_for('AdminView.AdminGroups'))
        flash('Successfully Created Group: {}'.format(Group.name), 'success')
        return redirect(url_for('AdminView.AdminGroup', id = Group.id))

@AdminView.route('/admin/groups/<id>')
@login_required
def AdminGroup(id):
    Group = GroupModel.query.filter_by(id = id).first()
    if Group is None:
        flash('Group {} not found'.format(id), 'danger')
        return redirect(url_for('AdminView.AdminGroups'))
    return render_template('admin/group.html', Group = Group)

@AdminView.route('/admin/users', methods=['GET', 'POST'])
@login_required
def AdminUsers():
    UserForm = CreateUserForm()
    if request.method == 'GET':
        Users = UserSQL.Friends(current_user.email)
        return render_template('admin/users.html', Users = Users,\
                               CreateUserForm = UserForm)
    if not UserForm.validate():
        flash('Error adding user', 'danger')
        return redirect(url_for('AdminView.AdminUsers'))
    try:
        user = UserSQL.Create(UserForm.Email.data)
        user.firstname = UserForm.Firstname.data
        user.lastname = UserForm.Lastname.data
        UserSQL.Save(user)
    except ValueError as e:
        flash('Error: {}'.format(e), 'danger')
        redirect(url_for('AdminView.AdminUsers'))
    flash('Successfully added user {}'.format(user.firstname), 'success')
    return redirect(url_for('AdminView.AdminUser', id = user.id))

@AdminView.route('/admin/users/<id>')
@login_required
def AdminUser(id):
    User = UserModel.query.filter_by(id = id).first()
    usersettings = UserSettings()
    userpassword = UserPassword()
    usergroupadd = UserGroupAdd()
    if User is None:
        flash('User {} not found'.format(id), 'danger')
        return redirect(url_for('AdminView.AdminGroups'))
    return render_template('admin/user.html', User = User, UserSettings =
                           usersettings, UserPassword = userpassword,
                           UserGroupAdd = usergroupadd)

@AdminView.route('/admin/backup')
@login_required
def AdminBackup():
    return render_template('admin/backup.html')


