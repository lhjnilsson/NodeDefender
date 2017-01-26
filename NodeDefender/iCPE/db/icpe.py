from . import redisconn
from .. import mqtt
from ...models.manage import icpe as iCPESQL
from ...models.manage import icpe as iCPERedis
from ... import celery
from datetime import datetime
from . import logger, Load

def Verfiy(mac, ipaddr = None, port = None):
    if len(iCPERedis.Get(mac)):
        return iCPERedis.Get(mac)
    else:
        if iCPESQL.Get(mac):
            return Load(iCPESQL.Get(mac))
        else:
            iCPESQL.Create(mac, ipaddr = ipaddr, port = port)
            mqtt.iCPE.Query(mac, ipaddr, port)

    return iCPERedis.Load(mac)


