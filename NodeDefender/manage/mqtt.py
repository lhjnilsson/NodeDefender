from flask_script import Manager, prompt
from ..models.manage import mqtt

manager = Manager(usage='Manage MQTT')

@manager.option('-i', '-ipaddr', '--ipaddr', dest='ipaddr', default=None)
@manager.option('-p', '-port', '--port', dest='port', default=None)
@manager.option('-u', '-username', '--username', dest='username', default=None)
@manager.option('-pw', '--password', dest='password', default=None)
def create(ipaddr, port, username, password):
    'Create Node and Assign to Group'
    if ipaddr is None:
        ipaddr = prompt('IP Address')
    
    if port is None:
        port = prompt('Port Number')
    
    '''
    if username is None:
        username = prompt('Username(blank for None)')
        if not len(username):
            username = None
    
    if password is None:
        password = prompt('Password(blank for None)')
        if not len(password):
            password = None
    '''

    try:
        mqtt.Create(ipaddr, port, username, password)
    except ValueError as e:
        print("Error: ", e)
        return

    print("MQTT {} Successfully created".format(ipaddr))


@manager.option('-i', '--ipaddr', dest='ipaddr', default=None)
def delete(ipaddr):
    'Delete Node'
    if ipaddr is None:
        ipaddr = prompt('IP Address')
    
    try:
         mqtt.Delete(ipaddr)
    except LookupError as e:
        print("Error: ", e)
        return

    print("Node {} Successfully deleted".format(name))

@manager.command
def list():
    for m in mqtt.List():
        print("ID: {}, IP: {}:{}".format(m.id, m.ipaddr, m.port))

