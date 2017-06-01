from flask_script import Manager, prompt
from ..models.manage import mqtt

manager = Manager(usage='Manage MQTT')

@manager.option('-h', '-host', '--host', dest='host', default=None)
@manager.option('-p', '-port', '--port', dest='port', default=None)
@manager.option('-u', '-username', '--username', dest='username', default=None)
@manager.option('-pw', '--password', dest='password', default=None)
def create(host, port, username, password):
    'Create Node and Assign to Group'
    if host is None:
        host = prompt('Host Address')
    
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
        mqtt.Create(host, port, username, password)
    except ValueError as e:
        print("Error: ", e)
        return

    print("MQTT {} Successfully created".format(host))


@manager.option('-i', '--host', dest='host', default=None)
def delete(host):
    'Delete Node'
    if host is None:
        host = prompt('Host Address')
    
    try:
         mqtt.Delete(host)
    except LookupError as e:
        print("Error: ", e)
        return

    print("MQTT {} Successfully deleted".format(host))

@manager.command
def list():
    for m in mqtt.List():
        print("ID: {}, IP: {}:{}".format(m.id, m.host, m.port))

