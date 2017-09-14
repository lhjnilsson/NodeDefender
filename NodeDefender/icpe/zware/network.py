import NodeDefender

OPERATION_MODES = {'0' : 'nop', '1' : 'initialize', '2' : 'include node',
                   '3' : 'exclude node', '4' : 'replace node', '5' : 'remove node',
                   '6' : 'initialize', '7' : 'update',
                   '8' : 'reset', '9' : 'migrate by SUC', '10' : 'migrate',
                   '11' : 'assign/deassign SUC/SIS', '13': 'update node',
                   '14' : 'send NIF',
                   '15' : 'network changed', '50' : 'zip&zware restart',
                   '51' : 'zware restart'}

def operation(icpe, mode, status):
    try:
        mode = OPERATION_MODES[str(mode)]
    except KeyError:
        mode = "Undefined"

    if status == '0':
        status = 'done'
    elif status == '255':
        status = 'failed'
    elif status == '254':
        status = 'started'
    elif status == '253':
        status = 'aborted'
    elif status > 251 and status < 250:
        status = 'intermediate'

    if mode == "remove node" and status == "done":
        NodeDefender.mqtt.command.icpe.zwave.node.list(icpe)
