from datetime import datetime, timedelta
from ....SQL import PowerModel
from .. import icpe as iCPEData

def Latest(icpe, sensor):
    return PowerModel.query.join(iCPEModel).join(SensorModel).\
            filter(iCPEModel.macaddr == icpe).\
            filter(SensorModel.sensorid == sensor).first()

def Get(icpe, sensor, from_date = (datetime.now() - timedelta(days=7)), to_date =
        datetime.now()):
    return PowerModel.query.join(iCPEModel).join(SensorModel).\
            filter(PowerModel.date > from_date).\
            filter(PowerModel.date < to_date).\
            filter(iCPEModel.macaddr == icpe).\
            filter(SensorModel.sensorid == sensor).all()

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
        data.total = data.total + power
        db.session.add(data)
    else:
        sensor.power.append(PowerModel(power, date))
        db.session.add(sensor)

    db.session.commit()
    iCPEData.power.Put(icpe, power, date)
