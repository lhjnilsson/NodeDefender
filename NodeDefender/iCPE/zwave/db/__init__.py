import json
from os.path import abspath, dirname, join
basedir = abspath(dirname(__file__))
zdb = {}

def SensorInfo(vendor, product):
    try:
        return zdb[vendor][product]
    except KeyError:
        print('--- ' + vendor + product)
        return None

with open(join(basedir, 'ZWaveDB.json')) as fr:
    zdb = json.load(fr)
