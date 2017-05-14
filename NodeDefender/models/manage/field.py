from ..SQL import iCPEModel, SensorModel, SensorClassModel, FieldModel
from ... import db
from . import cmdclass as CmdclassSQL

def List():
    return FieldModel.query.all()

def Add(icpe, sensor, cmdclass, name, type, readonly):
    cmdclass = \
    SensorClassModel.query.join(SensorModel).join(iCPEModel).\
            filter(SensorClassModel.classname == cmdclass).\
            filter(SensorModel.sensorid == sensor).\
            filter(iCPEModel.macaddr == icpe).first()
    
    sensor = cmdclass.sensor
    icpe = sensor.icpe
    if [f for f in cmdclass.fields if f.name == name]:
        return False
    
    field = FieldModel(name, type, readonly)
    icpe.fields.append(field)
    sensor.fields.append(field)
    cmdclass.fields.append(field)
    db.session.add(cmdclass)
    db.session.commit()
    return field

def Clear(icpe, sensor, cmdclass):
    cmdclass = CmdclassSQL.Get(icpe, sensor, cmdclass)
    if cmdclass is None:
        return False

    for field in cmdclass.fields:
        db.session.delete(field)

    db.session.commit()
    return True
