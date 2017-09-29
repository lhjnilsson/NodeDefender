from flask_mail import Message
from flask import render_template, url_for
import Nodedefender
from NodeDefender import serializer
from NodeDefender.mail import mail

@NodeDefender.decorators.mail_enabled
@NodeDefender.decorators.celery_task
def new_node(group, node):
    group = NodeDefender.db.group.get(group)
    if group is None:
        return False
    if group.email is None:
        return False
    
    node = NodeDefender.db.node.get(node)
    if node is None:
        return False

    msg = Message('Node added to {}'.format(group.name), sender='noreply@nodedefender.com',
                  recipients=[group.email])
    url = url_for('node_view.nodes_node', name = serializer.dumps(node.name))
    msg.body = render_template('mail/node/new_node.txt', node = node, url =
                              url)
    mail.send(msg)
    return True
