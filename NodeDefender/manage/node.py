from flask_script import Manager, prompt
from ..models.manage import node, icpe, node

manager = Manager(usage='Manage Nodes')

@manager.option('-name', '--name', dest='node', default=None)
@manager.option('-group', '--group', dest='group', default=None)
def create(node, group):
    'Create Node and Assign to Group'
    if node is None:
        node = prompt('Node Name')
    
    if group is None:
        group = prompt('Group Name')

    node.create(node, group)
    
    print("Node {} Successfully created".format(node))


@manager.option('-name', '--name', dest='node', default=None)
def delete(node):
    'Delete Node'
    if node is None:
        node = prompt('Node Name')

    node.delete(node)
    print("Node {} Successfully deleted".format(node))

@manager.option('-name', '--name', dest='node', default=None)
@manager.option('-group', '--group', dest='group', default=None)
def join(node, group):
    'Let a Node join a Group'
    if node is None:
        node = prompt("Node Name")

    if group is None:
        group = prompt("Group Name")

    node.join(node, group)

@manager.option('-name', '--name', dest='node', default=None)
@manager.option('-group', '--group', dest='group', default=None)
def leave(node, group):
    'Let a Node leave a Group'
    if node is None:
        node = prompt("Node Name")

    if group is None:
        group = prompt("Group Name")

    node.leave(node, group)

@manager.option('-name', '--name', dest='name', default=None)
def get(name):
    'Get a specific Node'
    if name is None:
        name = prompt("Node Name")
    
    node = node.Get(name)
    if node is None:
        print("Unable to find Node")
    
    print("ID: {}, Name: {}".format(node.id, node.name))
    

@manager.command
def list():
    'List avalible Nodes'
    for node in node.list():
        print("ID: {}, Alias: {}".format(node.id, node.alias))

@manager.option('-name', '--name', dest='name', default=None)
def groups(name):
    'Get Groups that a Node belongs to'
    if name is None:
        name = prompt("Node Name")

    for n in node.Groups(name):
        print("ID: {}, Name: {}".format(n.id, n.name))


@manager.option('-name', '--name', dest='name', default=None)
def icpes(name):
    'Get iCPEs that belong to Node'
    if name is None:
        name = prompt("Node Name")

    for n in node.iCPEs(name):
        print("ID: {}, Name: {}".format(n.id, n.name))
