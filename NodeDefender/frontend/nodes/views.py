from .. import NodeView
from flask import render_template, request
from .models import iCPEModel, NodeModel
from flask_security import login_required

@NodeView.route('/nodes/list', methods=['GET', 'POST'])
@login_required
def NodesList():
    if request.method == 'GET':
        return('OK')
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

@NodeView.route('/nodes/list/<mac>', methods=['GET', 'POST'])
@login_required
def NodesNode(mac):
    iCPE = iCPEModel.query.filter_by(mac = mac).first()
    if not iCPE:
        raise ValueError('Cant find mac')
    form = NodeForm()
    BasicForm = iCPEBasicForm()
    AddressForm = iCPEAddressForm()
    NodeBasic = NodeBasicForm()
    if request.method == 'GET':
        znodes = icpe.WebForm(mac)
        '''
        powerstat = dict((nodeid, list(events)) for nodeid, events in
                    groupby(iCPE.powerstat, lambda stat: stat.nodeid))
        '''
        return render_template('nodes/node.html', mac=mac, form=form, iCPE =
                               iCPE, znodes = znodes, iCPEBasicForm =
                               BasicForm, iCPEAddressForm = AddressForm,
                               NodeBasicForm = NodeBasic)
    elif request.method == 'POST':
        if BasicForm.validate_on_submit():
            iCPE.alias = BasicForm.alias.data
            iCPE.comment = BasicForm.comment.data
        elif AddressForm.validate_on_submit():
            iCPE.location.street = AddressForm.street.data
            iCPE.location.city = AddressForm.city.data
            iCPE.location.geolat = AddressForm.geolat.data
            iCPE.location.geolong = AddressForm.geolong.data
        
        db.session.add(iCPE)
        db.session.commit()
        return render_template('nodes/node.html', mac=mac, form=form, iCPE = iCPE,
                                iCPEAddressForm = AddressForm, iCPEBasicForm =
                                BasicForm, NodeBasicForm = NodeBasic)

@NodeView.route('/nodes/<mac>/<mode>')
@login_required
def NodesUpdate(mac):
    if not mqtt():
        flash('MQTT is Offline', 'danger')
    else:
        try:
            getattr(icpe, 'Node' + mode.capitalize)(mac)
            flash('Node ' + mac + ' succesfully updated.', 'success')
        except AttributeError:
            flash('Uknown Mode ' + mode, 'danger')
    return redirect(url_for('NodesNode',  mac=mac))

@NodeView.route('/nodes/list/<mac>/<nodeid>', methods=['GET', 'POST'])
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


@NodeView.route('/nodes/<mac>/notes/add', methods=['GET', 'POST'])
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

@NodeView.route('/nodes/<mac>/notes/sticky', methods=['GET', 'POST'])
@login_required
def NodesNoteSticky(mac):
    if request.method == 'POST':
        note = request.form['note']
        icpe = iCPEModel.query.filter_by(mac = mac).first()
        icpe.notesticky = note
        db.session.add(icpe)
        db.session.commit()
        return redirect(url_for('NodesNode', mac=mac))
    else:
        return redirect(url_for('NodesNode', mac=mac))

@NodeView.route('/nodes/<mac>/delete')
@login_required
def DeleteNode(mac):
    try:
        icpe.DeleteiCPE(mac)
        flash('Node: ' + mac + ' successfully deleted', 'success')
        return redirect(url_for('NodesList'))
    except Exception as e:
        flash('Unable to remove ' + str(mac) + '. Error: ' + str(e), 'danger')
        return redirect(url_for('NodesList'))

@NodeView.route('/nodes/<mac>/<nodeid>/<cls>/<field>/hide')
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

@NodeView.route('/nodes/<mac>/<nodeid>/<cls>/<field>/display')
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

