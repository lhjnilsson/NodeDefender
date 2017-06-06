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

from . import db, event, decorators
from .msgtype import cmd, err, rpt, rsp
