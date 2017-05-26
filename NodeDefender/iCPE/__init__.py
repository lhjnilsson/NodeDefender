from .. import celery, loggHandler
from ..models.manage import icpe as iCPESQL
from ..models.redis import field as FieldRedis
from ..models.redis import icpe as iCPERedis
from ..models.redis import sensor as SensorRedis
from ..models.redis import commandclass as CommandclassRedis
from celery.utils.log import get_task_logger
import logging

logger = logging.getLogger('iCPE')
logger.setLevel('INFO')
logger.addHandler(loggHandler)
log = get_task_logger(__name__)
log.addHandler(loggHandler)

def Load(icpes = None):
    '''
    Loads iCPEs and Sensors
    Tries to load commandclasses to sensor, recieved NotImplementedError from
    Redis- handler in the classname is not specific(the class is not
                                                    supported).
    if so it tries to add the class.
    '''
    if icpes is None:
        icpes = iCPESQL.List()
    
    for icpe in icpes:
        if not icpe.enabled:
            continue
        iCPERedis.Load(icpe)
        for sensor in icpe.sensors:
            SensorRedis.Load(sensor)
            for cc in sensor.commandclasses:
                if not cc.supported:
                    continue

                CommandclassRedis.Load(cc)

                if not cc.types:
                    field = eval('zwave.commandclasses.'+cc.name+'.Fields')()
                    FieldRedis.Load(sensor, cc, field)
                    continue
                
                for t in cc.types:
                    if not t.supported:
                        continue
                    field = eval('zwave.commandclasses.'+cc.name+'.'+t.name+\
                                 '.Fields')()
                    FieldRedis.Load(sensor, cc, field)

from . import db, event, decorators
from .msgtype import cmd, err, rpt, rsp
