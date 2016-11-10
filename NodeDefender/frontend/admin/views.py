from . import AdminView

@AdminView.route('/admin/server')
@login_required
def AdminServer():
    if request.method == 'GET':
        sform = AdminServerForm()
        return render_template('admin/server.html', sform = sform)

@AdminView.route('/admin/sever/setgeneral', methods=['GET', 'POST'])
@login_required
def AdminServerSetGeneral():
    sform = AdminServerForm(request.form)
    if sform.validate():
        flash('Successfully updated General Settings', 'success')
        return redirect(url_for('AdminServer'))
    else:
        flash('Error when trying to update General Settings', 'danger')
        return redirect(url_for('AdminServer'))

@AdminView.route('/admin/users')
@login_required
def AdminUsers():
    return render_template('admin/users.html')

@AdminView.route('/admin/mqtt')
@login_required
def AdminMqtt():
    return render_template('admin/mqtt.html')

@AdminView.route('/admin/backup')
@login_required
def AdminBackup():
    return render_template('admin/backup.html')


