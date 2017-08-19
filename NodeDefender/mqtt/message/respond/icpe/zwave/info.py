from NodeDefender import db

def qry(topic, payload):
    data = payload
    operation, status = data['stat'].split(',')
    data.pop('stat')
    data['operation'] = operation
    data['status'] = status
    return db.icpe.update(topic['macAddress'], **data)
