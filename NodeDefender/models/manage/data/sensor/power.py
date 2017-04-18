from datetime import datetime, timedelta
from ....SQL import PowerModel, iCPEModel, SensorModel
from .. import icpe as iCPEData
from ..... import db

def Latest(icpe, sensor):
    power_data = PowerModel.query.join(iCPEModel).join(SensorModel).\
            filter(iCPEModel.macaddr == icpe).\
            filter(SensorModel.sensorid == sensor).first()

    if not power_data:
        return False

    return {'icpe' : icpe, 'sensor' : sensor, 'date' : str(power_data.date),\
            'low' : power_data.low, 'high' : power_data.high, \
            'total' : power_data.total}

def Get(icpe, sensor, from_date = (datetime.now() - timedelta(days=7)), to_date =
        datetime.now()):
    power_data =  PowerModel.query.join(iCPEModel).join(SensorModel).\
            filter(PowerModel.date > from_date).\
            filter(PowerModel.date < to_date).\
            filter(iCPEModel.macaddr == icpe).\
            filter(SensorModel.sensorid == sensor).all()

    if not power_data:
        return False

    ret_json = {'icpe' : icpe}
    ret_json['sensor'] = sensor
    ret_json['power'] = []
    for data in power_data:
        ret_json['power'].append({'date' : str(data.date), 'low' : data.low, 'high' :
                                               data.high, 'total' :
                                               data.total})
    return ret_json

def Put(icpe, sensor, power, date = datetime.now()):
    date = date.replace(minute=0, second=0, microsecond=0)
    data = PowerModel.query.join(iCPEModel).join(SensorModel).\
            filter(PowerModel.date == date).\
            filter(iCPEModel.macaddr == icpe).\
            filter(SensorModel.sensorid == sensor).first()
    sensor = SensorModel.query.join(iCPEModel).\
            filter(SensorModel.sensorid == sensor).\
            filter(iCPEModel.macaddr == icpe).first()

    if data:
        if power > data.high:
            data.high = power
        
        if power < data.low or data.low == 0:
            data.low = power

        data.average = (data.average + power) / 2
        data.total = data.total + power
        db.session.add(data)
    else:
        data = PowerModel(power, date)
        data.sensor = sensor
        data.icpe = sensor.icpe
        db.session.add(data)

    db.session.commit()
