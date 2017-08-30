from NodeDefender.icpe.zwave.commandclass import alarm, basic, bswitch,\
        meter, msensor

classnumbers = {'71': 'alarm', '20' : 'basic', '25' : 'bswitch'}

def to_name(classnumber):
    try:
        return classnumbers[classnumber]
    except KeyError:
        return False

def to_number(classname):
    try:
        return eval(classname + '.number')()
    except NameError:
        return False

def info(classnumber = None, classname = None, classtype = None):
    if classnumber and not classname:
        classname = to_name(classnumber)
        if not classname:
            return None
    
    if not classtype:
        try:
            return eval(classname + '.info')
        except NameError:
            return None

    try:
        typename = eval(classname + '.classtypes')[classtype]
    except KeyError:
        return None

    try:
        return eval(classname + '.' + typename + '.info')
    except NameError:
        return None
