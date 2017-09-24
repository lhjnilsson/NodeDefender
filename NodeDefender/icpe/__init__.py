import logging
from NodeDefender import loggHandler

logger = logging.getLogger('iCPE')
logger.setLevel('INFO')
logger.addHandler(loggHandler)

from NodeDefender.icpe import zwave, system, sensor
