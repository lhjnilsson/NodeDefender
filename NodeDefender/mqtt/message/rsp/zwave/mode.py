def qry(topic, payload):
    return icpe.state(topic['icpe'], payload)

def include(topic, payload):
    return icpe.state(topic['icpe'], 'include')

def exclude(topic, payload):
    return icpe.state(topic['icpe'], 'exclude')

def normal(topic, payload):
    return icpe.state(topic['icpe'], 'normal')

