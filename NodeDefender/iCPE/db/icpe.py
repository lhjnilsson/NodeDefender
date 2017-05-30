from . import redisconn
from .. import mqtt
from ...models.manage import icpe as iCPESQL
from ...models.redis import icpe as iCPERedis
from ...mail import icpe as iCPEMail
from ... import celery
from datetime import datetime
from . import logger

def Verify(topic, payload, mqttsrc = None):
    if len(iCPERedis.Get(topic.macaddr)):
        return iCPERedis.Get(topic.macaddr)
    else:
        if iCPESQL.Get(topic.macaddr):
            if iCPESQL.Enabled(topic.macaddr):
                return iCPERedis.Load(topic.macaddr)
            else:
                iCPESQL.Enable(topic.macaddr **mqttsrc)
                iCPEMail.icpe_enabled.apply_async((topic.macaddr,
                                               mqttsrc['ipaddr'],
                                               mqttsrc['port']), countdown=30)
                return iCPERedis.Load(topic.macaddr)
        else:
            iCPESQL.Create(topic.macaddr)
            iCPESQL.Enable(topic.macaddr, **mqttsrc)
            iCPEMail.new_icpe.apply_async((topic.macaddr, mqttsrc['ipaddr'],
                                           mqttsrc['port']), countdown=30)
            iCPERedis.Load(topic.macaddr)
    return mqtt.icpe.Query(topic.macaddr, **mqttsrc)

@celery.task
def Load(group = None):
    for icpe in iCPESQL.List():
        iCPERedis.Load(icpe)
    return True

