topic = namedtuple("topic", "mac msgtype nodeid cmdclass action")

def TopicToTuple(func):
    '''
    Takes a XML from MQTT and zips it into a Dictonary following the Common
    Message Format for iCPE
    '''
    @wraps(func)
    def zipper(*args, **kwargs):
        arg1 = dict(zip(CommonFormat, args[1]))
        splitted = args[1].split('/')
        args[1] = topic(splitted[1][2:], # Mac, minus the 0x
                       splitted[2], # Msgtype
                       splitted[4], # NodeID
                       splitted[6], # CommandClass
                       splitted[8]) # Action
        return func(args)
    return zipper

def JSONToDict(func):
    pass
