def qry(topic, payload):
    operation, status = payload['stat'].split(',')
    netid = payload['netid']
    controllerid = payload['controllerid']
    nodelist = payload['nodebmp']
