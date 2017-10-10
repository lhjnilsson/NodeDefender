import flask_script
import re

manager = flask_script.Manager(usage="Setup NodeDefender Configuration")

@manager.command
def all():
    general()
    database()
    mail()
    logging()
    celery()
    print_topic("Configuration Successfully stored!")
    print("Dont forget to migrate and upgrade the database before running")
    print("./manage.py db migrate")
    print("./manage.py db upgrade")
    return True

def get_chunks(message):
    return [ message[i:i+38] for i in range(0, len(message), 38)]

def print_message(message):
    print("#")
    if len(message) > 38:
        for chunk in get_chunks(message):
            print("#" +  chunk.center(38))
    else:
        print("#" + message.center(38))
    print("#")
    return True

def print_topic(topic):
    print("****************************************")
    print("*" + topic.center(38) + "*")
    print("****************************************")
    return True

def print_info(message):
    for part in message.split('.'):
        print("/ ", re.sub(' +', ' ', part))

import NodeDefender.manage.setup.celery
import NodeDefender.manage.setup.database
import NodeDefender.manage.setup.general
import NodeDefender.manage.setup.logging
import NodeDefender.manage.setup.mail
