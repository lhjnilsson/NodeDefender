from NodeDefender.db.sql import SQL, MQTTModel, GroupModel, iCPEModel
from redlock import RedLock

def get_sql(host, port = 1883):
    return MQTTModel.query.filter_by(host = host, port = port).first()

def update_sql(host, port = 1883, **kwargs):
    mqtt = get_sql(host, port)
    if mqtt is None:
        return False

    for key, value in kwargs:
        if key not in mqtt.columns():
            continue
        setattr(mqtt, key, value)

    SQL.session.save(mqtt)
    SQL.session.comit()
    return mqtt

def create_sql(host, port = 1883):
    if get_sql(host, port):
        return False
    
    mqtt = MQTTModel(host, port)
    SQL.session.add(mqtt)
    SQL.session.commit()
    return mqtt

def delete_sql(host, port = 1883):
    mqtt = get_sql(host, port)
    if mqtt is None:
        return False
    SQL.session.delete(mqtt)
    return SQL.session.commit()

def get(host, port = 1883):
    return get_sql(host, port)

def online(host, port):
    return False

def icpe(macaddr):
    return SQL.session.query(MQTTModel).join(MQTTModel.icpes).\
            filter(iCPEModel.macaddr == macaddr).first().to_json()

def create(host, port = 1883):
    return create_sql(host, port)

def delete(host, port = 1883):
    return delete_sql(host, port)

def list(group = None, icpe = None):
    if group:
        return [mqtt.to_json() for mqtt in \
                db.session.query(MQTTModel).join(MQTTModel.group).\
                filter(GroupModel.name == group).all()]
    if icpe:
        return [mqtt.to_json() for mqtt in \
                db.session.query(MQTTModel).join(MQTTModel.icpe).\
                filter(iCPEModel.macaddr == icpe).all()]
    return [mqtt.to_json() for mqtt in MQTTModel.query.all()]
