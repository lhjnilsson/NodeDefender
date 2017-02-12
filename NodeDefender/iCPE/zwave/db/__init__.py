import json
zdb = {}

def SensorInfo(vendor, product):
    try:
        info = zdb[vendor][product]
    except KeyError:
        return None

with open('ZWaveDB.json') as fr:
    zdb = json.load(fr)
