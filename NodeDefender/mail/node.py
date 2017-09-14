from ..models.manage import group as GroupSQL
from ..models.manage import node as NodeSQL
from .. import serializer, app, celery
from . import mail
from flask_mail import Message
from flask import render_template, url_for

@celery.task
def new_node(group, node):
    group = GroupSQL.Get(group)
    if group is None:
        return False
    if group.email is None:
        return False
    
    node = NodeSQL.Get(node)
    if node is None:
        return False

    msg = Message('Node added to {}'.format(group.name), sender='noreply@nodedefender.com',
                  recipients=[group.email])
    url = url_for('node_view.nodes_node', name = serializer.dumps(node.name))
    msg.body = render_template('mail/node/new_node.txt', node = node, url =
                              url)
    mail.send(msg)
    return True
