from flask_script import Manager, prompt
from ..models.manage import node, icpe

manager = Manager(usage='Manage iCPE Devices')

@manager.option('-m', '--mac', dest='mac', default=None)
@manager.option('-n', '--node', dest='node', default=None)
def create(mac, node):
    'Create iCPE'
    if mac is None:
        mac = prompt('Mac')

    if node is None:
        node = prompt('Node')

    try:
        icpe.Create(mac, node)
    except (LookupError, ValueError) as e:
        print("Error: ", str(e))
        return

    print('iCPE {} Successfully Created'.format(mac))
    return

@manager.option('-m', '--mac', dest='mac', default=None)
def delete(mac):
    'Remove iCPE'
    if mac is None:
        mac = prompt('Mac')

    try:
        icpe.Delete(mac)
    except LookupError as e:
        print("Error: ", str(e))
        return

    print("Successfully Deleted: ", mac)

'''
@manager.option('-mac', '--mac', dest='mac', default=None)
def join(icpe, group):
    'Let iCPE Join a Group'
    if mac is None:
        mac = prompt('Mac')
    
    if node is None:
        node = prompt('Group')

    icpe.Join(mac, group)

@manager.option('-mac', '--mac', dest='mac', default=None)
def leave(icpe, group):
    'Let iCPE Leave a Group'
    if mac is None:
        mac = prompt('Mac')
    
    if node is None:
        node = prompt('Group')

    icpe.Leave(mac, group)
'''


@manager.command
def list():
    'List iCPEs'
    for i in icpe.List():
        print("ID: {}, Name: {}, MAC: {}".format(i.id, i.name,
                                                  i.mac))

@manager.option('-mac', '--mac', dest='mac', default=None)
def info(mac):
    'Info about a specific iCPE'
    if mac is None:
        mac = prompt('Mac')
    
    icpe = icpe.Get(mac)
    if icpe is None:
        print("Unable to find iCPE {}".format(mac))

    print('ID: {}, MAC: {}'.format(icpe.id, icpe.mac))
    print('Alias {}, Node: {}'.format(icpe.alias, icpe.node.name))
    print('ZWave Sensors: ')
    for sensor in iCPE.sensors:
        print('Alias: {}, Type: {}'.format(sensor.alias, sensor.type))
