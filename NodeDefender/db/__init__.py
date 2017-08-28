import logging
import NodeDefender.db.sql
import NodeDefender.db.redis
from NodeDefender import loggHandler

logger = logging.getLogger('db')
logger.setLevel('DEBUG')
logger.addHandler(loggHandler)

from NodeDefender.db import group, user, node, icpe, sensor, mqtt, \
        commandclass, field
