from datetime import datetime, timedelta
from ....SQL import PowerModel
from .. import icpe as iCPEData

def Latest(icpe, sensor):
    return PowerModel.query.filter_by(node = None, icpe = icpe, sensor = sensor).first()

def Get(icpe, sensor, from_date = (datetime.now() - timedelta(days=7)), to_date =
        datetime.now()):
    return session.query(PowerModel).filter(node == None, icpe == icpe, sensor == None, date > from_date, date
                                            < to_date)

def Put(icpe, sensor, power, date = datetime.now()):
    date = date.replace(minute=0, second=0, microsecond=0)
    data, icpe, sensor = PowerModel.query.join(iCPEModel).join(SensorModel).\
            filter(PowerModel.date == date).\
            filter(iCPEModel.macaddr == icpe).\
            filter(SensorModel.sensorid == sensor).first()

    if data:
        if power > data.power:
            data.high = power
        
        if power < data.power:
            data.low = power

        data.average = (data.average + power) / 2
        db.session.add(data)
    else:
        sensor.power.append(PowerModel(power, date))
        db.session.add(sensor)

    db.session.commit()
    iCPEData.power.Put(icpe, power, date)
