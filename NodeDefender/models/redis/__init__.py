from redis import ConnectionPool, StrictRedis
from functools import wraps
from ... import loggHandler
import logging

pool = ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)

logger = logging.getLogger('Redis')
logger.setLevel('INFO')
logger.addHandler(loggHandler)


def redisconn(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = StrictRedis(connection_pool=pool)
        return func(*args, conn = conn, **kwargs)
    return wrapper

from . import sensor, icpe, cmdclass
