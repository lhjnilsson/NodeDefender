import NodeDefender

TopicFormat = "icpe/0x{}/cmd/node/{}/class/{}/act/{}"

def fire(topic, payload = None, icpe = None, mqttsrc = None):
    if icpe is None and mqttsrc is None:
        raise ValueError("Need either iCPE or MQTT Source to target")

    if mqttsrc is None and icpe:
        mqttsrc = NodeDefender.db.mqtt.icpe(icpe)

    conn = NodeDefender.mqtt.connection.connection(mqttsrc['host'], \
                                                   mqttsrc['port'])
    return conn.publish(topic, payload)

import NodeDefender.mqtt.command.icpe
import NodeDefender.mqtt.command.sensor
import NodeDefender.mqtt.command.commandclass
