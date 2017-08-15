import json
from os.path import abspath, dirname, join
basedir = abspath(dirname(__file__))
zdb = {}

def info(vendorid, productid):
    try:
        return zdb[vendorid][productid]
    except KeyError:
        print('--- ' + vendorid + productid)
        return None

with open(join(basedir, 'ZWaveDB.json')) as fr:
    zdb = json.load(fr)
