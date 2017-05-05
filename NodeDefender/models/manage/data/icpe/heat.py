from datetime import datetime, timedelta
from ....SQL import HeatModel, iCPEModel
from ..... import db
from sqlalchemy import func
from sqlalchemy.sql import label

def Latest(icpe):
    heat_data = db.session.query(HeatModel, \
                                  label('low', func.min(HeatModel.low)),
                                  label('high', func.max(HeatModel.high)),
                                  label('total', func.sum(HeatModel.average)),
                                  label('date', HeatModel.date)).\
            join(iCPEModel).\
            filter(iCPEModel.macaddr == icpe).\
            order_by(HeatModel.date.desc()).\
            group_by(HeatModel.date).first()

    if not heat_data:
        return False
    
    return {'icpe' : icpe, 'date' : str(heat_data.date), 'low' : power_data.low,\
            'high' : heat_data.high, 'total' : power_data.total}

def Get(icpe, from_date = (datetime.now() - timedelta(days=7)), to_date =
        datetime.now()):
    heat_data = db.session.query(HeatModel, \
                                  label('low', func.min(HeatModel.low)),
                                  label('high', func.max(HeatModel.high)),
                                  label('total', func.sum(HeatModel.average)),
                                  label('date', HeatModel.date)).\
            join(iCPEModel).\
            filter(iCPEModel.macaddr == icpe).\
            filter(HeatModel.date > from_date).\
            filter(HeatModel.date < to_date).\
            group_by(HeatModel.date).all()

    if not heat_data:
        return False

    ret_json = {'icpe' : icpe}
    ret_json['heat'] = []
    for data in heat_data:
        ret_json['heat'].append({'date' : str(data.date), 'low' : data.low, 'high' : data.high,
                                    'total' : data.total})
    return ret_json
