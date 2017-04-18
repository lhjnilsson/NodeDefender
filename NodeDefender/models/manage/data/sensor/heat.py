from datetime import datetime, timedelta
from ....SQL import HeatModel, iCPEModel, SensorModel
from .. import icpe as iCPEData
from ..... import db

def Latest(icpe, sensor):
    heat_data = HeatModel.query.join(iCPEModel).join(SensorModel).\
            filter(iCPEModel.macaddr == icpe).\
            filter(SensorModel.sensorid == sensor).first()

    if not heat_data:
        return False

    return {'icpe' : icpe, 'sensor' : sensor, 'date' : heat_data.date,\
            'low' : heat_data.low, 'high' : heat_data.high, \
            'total' : heat_data.total}

def Get(icpe, sensor, from_date = (datetime.now() - timedelta(days=7)), to_date =
        datetime.now()):
    heat_data =  HeatModel.query.join(iCPEModel).join(SensorModel).\
            filter(HeatModel.date > from_date).\
            filter(HeatModel.date < to_date).\
            filter(iCPEModel.macaddr == icpe).\
            filter(SensorModel.sensorid == sensor).all()

    if not heat_data:
        return False

    ret_json = {'icpe' : icpe}
    ret_json['sensor'] = sensor
    ret_json['heat'] = []
    for data in heat_data:
        ret_json['heat'].append({data.date : {'low' : data.low, 'high' :
                                               data.high, 'total' :
                                               data.total}})
    return ret_json

def Put(icpe, sensor, heat, date = datetime.now()):
    date = date.replace(minute=0, second=0, microsecond=0)
    data = HeatModel.query.join(iCPEModel).join(SensorModel).\
            filter(HeatModel.date == date).\
            filter(iCPEModel.macaddr == icpe).\
            filter(SensorModel.sensorid == sensor).first()
    sensor = SensorModel.query.join(iCPEModel).\
            filter(SensorModel.sensorid == sensor).\
            filter(iCPEModel.macaddr == icpe).first()

    if data:
        if heat > data.high:
            data.high = heat
        
        if heat < data.low or data.low == 0:
            data.low = heat

        data.average = (data.average + heat) / 2
        data.total = data.total + heat
        db.session.add(data)
    else:
        data = HeatModel(heat, date)
        data.sensor = sensor
        data.icpe = sensor.icpe
        db.session.add(data)

    db.session.commit()
