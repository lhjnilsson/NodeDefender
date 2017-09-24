import NodeDefender

def commandclasses(icpe, sensorid, *commandclasses):
    known_classes = [commandclass.number for commandclass in \
                     NodeDefender.db.commandclass.list(icpe, sensorid)]
    
    
    for commandclass in commandclasses:
        if commandclass not in known_classes:
            NodeDefender.db.commandclass.create(icpe, sensorid, commandclass)

    for commandclass in known_classes:
        if commandclass not in commandclasses:
            NodeDefender.db.commandclass.delete(icpe, sensorid, commandclass)
    return True

def commandclass_types(icpe, sensorid, commandclass_name, *classtypes):
    known_types = NodeDefender.db.commandclass.\
            get_sql(icpe, sensorid, commandclass_name).commandclasstypes()

    for classtype in classtypes:
        if classtype not in known_types:
            NodeDefender.db.commandclass.add_type(icpe, sensorid,
                                                  commandclass_name, classtype)

    return True
