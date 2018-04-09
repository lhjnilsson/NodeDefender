import NodeDefender.mqtt.message
import NodeDefender.mqtt.command
from NodeDefender.mqtt import connection

logger = None

def load(loggHandler):
    global logger
    logger = NodeDefender.logger.getChild("MQTT")
    connection.load()
    logger.debug("MQTT Loaded")
    return True
