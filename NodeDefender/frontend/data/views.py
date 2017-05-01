from .. import DataView
from .models import *
from flask import request, render_template
from ... import serializer
from flask_login import login_required, current_user
from ...models.manage import group as GroupSQL
from ...models.manage import node as NodeSQL
from ...models.manage import sensor as SensorSQL

#Power
@DataView.route('/data/power')
@login_required
def DataPower():
    if request.method == 'GET':
        if current_user.superuser:
            groups = GroupSQL.List()
        else:
            groups = [group for group in current_user.groups]
        return render_template('data/power.html', groups = groups)

@DataView.route('/data/power/group/<name>')
def PowerGroup(name):
    name = serializer.loads(name)
    if request.method == 'GET':
        group = GroupSQL.Get(name)
        if group is None:
            pass # Fix later..
        return render_template('data/group/power.html', group = group)

@DataView.route('/data/power/node/<name>')
def PowerNode(name):
    name = serializer.loads(name)
    if request.method == 'GET':
        node = NodeSQL.Get(name)
        return render_template('data/node/power.html', node = node)

@DataView.route('/data/power/sensor/<icpe>/<sensor>')
def PowerSensor(icpe, sensor):
    icpe = serializer.loads(icpe)
    
    if request.method == 'GET':
        sensor = SensorSQL.Get(icpe, sensor)
        return render_template('data/sensor/power.html', sensor = sensor)

