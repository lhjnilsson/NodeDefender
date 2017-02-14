from . import redisconn
from .. import mqtt
from ...models.manage import icpe as iCPESQL
from ...models.redis import icpe as iCPERedis
from ... import celery
from datetime import datetime
from . import logger, Load

def Verify(topic, payload, mqttsrc = None):
    if len(iCPERedis.Get(topic.macaddr)):
        return iCPERedis.Get(topic.macaddr)
    else:
        if iCPESQL.Get(topic.macaddr):
            return iCPERedis.Load(topic.macaddr)
        else:
            iCPESQL.Create(topic.macaddr, **mqttsrc)
            iCPERedis.Load(topic.macaddr)
    return mqtt.icpe.Query(topic.macaddr, **mqttsrc)
