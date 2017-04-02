from . import mail
from ..models.SQL import GroupModel

@celery.task
def new_group(group):
    group = GroupSQL.Get(group)
    if group is None:
        return False
    if group.email is None:
        return False

    template = render_template('mail/group/new_group.txt', group = group)
    subject = 'Group Created'
    send_email(group.email, subject, template)
    return True

@celery.task
def new_node(group, node):
    group = GroupSQL.Get(group)
    if group is None:
        return False
    if group.email is None:
        return False

    template = render_template('mail/group/new_group.txt', group = group)
    subject = 'Group Created'
    send_email(group.email, subject, template)
    return True

@celery.task
def new_icpe(group, icpe):
    group = GroupSQL.Get(group)
    if group is None:
        return False
    if group.email is None:
        return False

    template = render_template('mail/group/new_group.txt', group = group)
    subject = 'Group Created'
    send_email(group.email, subject, template)
    return True

@celery.task
def new_mqtt(group, mqtt):
    group = GroupSQL.Get(group)
    if group is None:
        return False
    if group.email is None:
        return False

    template = render_template('mail/group/new_group.txt', group = group)
    subject = 'Group Created'
    send_email(group.email, subject, template)
    return True
