from flask_script import Manager, prompt
from ..models.manage import group

manager = Manager(usage='Manage Groups')

@manager.option('-name', '--name', dest='name', default=None)
@manager.option('-desc', '--description', dest='description', default=None)
def create(name, description):
    'Create a Group'
    if name is None:
        name = prompt('Group Name')
    
    if description is None:
        description = prompt('Description')

    group.Create(name, description)
    print("Group {} successfully added".format(name))

@manager.option('-name', '--name', dest='name', default=None)
def delete(name):
    'Delete a Group'
    if name is None:
        name = prompt('Group Name')

    group.Delete(name)
    print("Group {} successfully deleted".format(name))

@manager.command
def list():
    'List Groups'
    for g in group.List():
        print("ID: {}, Name: {}".format(g.id, g.name))

@manager.option('-name', '--name', dest='name', default=None)
def info(name):
    'Show information about a Group'
    if name is None:
        name = prompt('Group Name')

    g = group.Get(name)
    print("ID: {}, Name: {}".format(g.id, g.name))
    print("Description: {}".format(g.description))
    print("User Members:")
    for user in g.users:
        print("ID: {}, Mail: {}".format(user.id, user.mail))
    print("Nodes")
    for node in g.nodes:
        print("ID: {}, Name: {}".format(node.id, node.name))
