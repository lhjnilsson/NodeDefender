def XMLToDict(func):
    '''
    Takes a XML from MQTT and zips it into a Dictonary following the Common
    Message Format for iCPE
    '''
    @wraps(func)
    def zipper(*args, **kwargs):
        CommonFormat = ['icpe', 'mac', 'msgtype', 'node', 'nodeid', 'class',
                        'cmdclass', 'act', 'action']
        arg1 = dict(zip(CommonFormat, args[1]))

        return func(args[0], arg1, args[2], **kwargs)
    return zipper

def JSONToDict(func):
    pass
