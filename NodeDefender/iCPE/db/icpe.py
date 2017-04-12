from . import redisconn
from .. import mqtt
from ...models.manage import icpe as iCPESQL
from ...models.redis import icpe as iCPERedis
from ...mail import icpe as iCPEMail
from ... import celery
from datetime import datetime
from . import logger, Load

def Verify(topic, payload, mqttsrc = None):
    if len(iCPERedis.Get(topic.macaddr)):
        return iCPERedis.Get(topic.macaddr)
    else:
        if iCPESQL.Get(topic.macaddr):
            if iCPE.Enabled(topic.macaddr):
                return iCPERedis.Load(topic.macaddr)
            else:
                iCPE.Enable(topic.macaddr **mqttconn)
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
