def Event(payload):
    payload._retdata['watt'] = int(payload.data32, 0) / 10
    return payload
