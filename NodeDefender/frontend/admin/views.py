from .. import AdminView
from .forms import GeneralForm, CreateUserForm, CreateGroupForm
from flask_login import login_required, current_user
from flask import Blueprint, request, render_template
from ...models.manage import user as UserSQL
from ...models.manage import group as GroupSQL

@AdminView.route('/admin/server', methods=['GET', 'POST'])
@login_required
def AdminServer():
    General = GeneralForm()
    if request.method == 'GET':
        return render_template('admin/server.html', GeneralForm = GForm)
    
    if sform.validate():
        flash('Successfully updated General Settings', 'success')
        return redirect(url_for('AdminServer'))
    else:
        flash('Error when trying to update General Settings', 'danger')
        return redirect(url_for('AdminServer'))

@AdminView.route('/admin/groups', methods=['GET', 'POST'])
@login_required
def AdminGroups():
    GroupForm = CreateGroupForm()
    groups = GroupSQL.List()
    if request.method == 'GET':
        return render_template('admin/groups.html', groups = groups,
                                CreateGroupForm = GroupForm)
    else:
        GroupForm.validate_on_submit()
        Group = GroupSQL.Create(GroupForm.Name.data, GroupForm.Description.data)
        Group.email = GroupForm.Email.data
        GroupSQL.Save(Group)
        flash('Successfully Created Group: {}'.format(Group.Name), 'success')
        return redirect(url_for('AdminView.AdminGroups'))

@AdminView.route('/admin/groups/<name>')
@login_required
def AdminGroupsGroup(name):
    Group = GroupSQL.Get(name)
    if Group is None:
        flash('Group {} not found'.format(name), 'danger')
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
    user = UserSQL.Create(UserForm.Email.data)
    user.firstname = UserForm.Firstname.data
    user.lastname = UserForm.Lastname.data
    UserSQL.Save(user)
    flash('Successfully added user {}'.format(user.firstname), 'danger')
    return redirect(url_for('AdminView.AdminUsers'))

@AdminView.route('/admin/mqtt')
@login_required
def AdminMqtt():
    return render_template('admin/mqtt.html')

@AdminView.route('/admin/backup')
@login_required
def AdminBackup():
    return render_template('admin/backup.html')


