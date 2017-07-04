from flask_script import Manager, prompt
from ..models.manage import node, icpe

manager = Manager(usage='Manage iCPE Devices')

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

@manager.command
def list():
    'List iCPEs'
    icpes = icpe.List()
    if not icpes:
        print("No icpes")
        return False

    for i in icpes:
        print("ID: {}, MAC: {}".format(i.id, i.macaddr))
    return True

@manager.command
def unassigned():
    icpes = icpe.Unassigned()
    if not icpes:
        print("No Unassigned iCPEs")
        return False

    for i in icpes:
        print("ID: {}, MAC: {}".format(i.id, i.macaddr))
    return True

@manager.option('-mac', '--mac', dest='mac', default=None)
def info(mac):
    'Info about a specific iCPE'
    if mac is None:
        mac = prompt('Mac')
    
    icpe = icpe.Get(mac)
    if icpe is None:
        print("Unable to find iCPE {}".format(mac))

    print('ID: {}, MAC: {}'.format(icpe.id, icpe.macaddr))
    print('Alias {}, Node: {}'.format(icpe.alias, icpe.node.name))
    print('ZWave Sensors: ')
    for sensor in iCPE.sensors:
        print('Alias: {}, Type: {}'.format(sensor.alias, sensor.type))
