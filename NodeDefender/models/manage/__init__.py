from ... import loggHandler
import logging

logger = logging.getLogger('SQL')
logger.setLevel('INFO')
logger.addHandler(loggHandler)

from . import *
