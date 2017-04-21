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

    return {'icpe' : icpe, 'sensor' : sensor, 'date' : str(heat_data.date),\
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
        ret_json['heat'].append({'date' : str(data.date), 'low' : data.low, 'high' :
                                               data.high, 'total' :
                                               data.total})
    return ret_json

def Put(icpe, sensor, heat, date = None):
    if date is None:
        date = datetime.now().replace(minute=0, second=0, microsecond=0)
    
    icpe, sensor = db.session.query(iCPEModel, SensorModel).\
            filter(iCPEModel.macaddr == icpe).\
            filter(SensorModel.sensorid == sensor).first()
    
    if not icpe or not sensor:
        return False

    data = db.session.query(HeatModel).\
            filter(HeatModel.icpe == icpe,\
                   HeatModel.sensor == sensor,\
                   HeatModel.date == date).first()


    if data:
        if heat > data.high:
            data.high = heat
        
        if heat < data.low or data.low == 0:
            data.low = heat

        data.average = (data.average + heat) / 2
        db.session.add(data)
    else:
        data = HeatModel(heat, date)
        data.sensor = sensor
        data.icpe = sensor.icpe
        db.session.add(data)

    db.session.commit()
