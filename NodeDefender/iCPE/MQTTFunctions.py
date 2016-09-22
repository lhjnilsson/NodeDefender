'''
Copyright (c) 2016 Connection Technology Systems Northern Europe

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE
SOFTWARE.
'''
from functools import wraps
from ..models import iCPEModel, NodeModel
from datetime import datetime
from .. import db, outMQTTQueue
from . import PepperDB

class MQTTFunctions:
    '''
    Support Functions for iCPE regarding MQTT Connetion
    '''
    def logged(func):
        @wraps(func)
        def logger(*args, **kwargs):
            icpe = iCPEModel.query.filter_by(mac = args[1]['mac'][2:]).first()
            if not icpe:
                return func(*args, **kwargs)
            icpe.online = True
            icpe.last_online = datetime.now()
            db.session.add(icpe)
            db.session.commit()
            return func(*args, **kwargs)
        return logger
    
    def todict(func):
        @wraps(func)
        def dicter(*args, **kwargs):
            CMF = ['icpe', 'mac', 'msgtype', 'node', 'nodeid', 'class',
                   'cmdclass', 'act', 'action'] # Common Message Format
            _arg1 = dict(zip(CMF, args[1]))
            
            return func(args[0], _arg1, args[2], **kwargs)
        return dicter


    def cmd(self, topic, payload):
        '''
        commands sent to iCPE from NodeDefender or others
        '''
        pass

    @todict
    @logged
    def rsp(self, topic, payload):
        '''
        respond from iCPE for a call
        '''
        getattr(self, topic['act']+topic['action'])(topic, payload)
        return True

    @todict
    @logged
    def rpt(self, topic, payload):
        '''
        report from iCPE
        '''
        known = self.__contains__(topic['nodeid'])
        if not known:
            return
        result = known.callback(topic, self.PayloadToDict(payload))
        if result is not None:
            NodeLogQueue.put(('ZWaveEvent', {'action' : result, 'mac' : self.mac, 'nodeid'
                              : known.nodeid}))
            outSocketQueue.put(('roomevent', {'nodeid' : topic['nodeid'], 'action' :
                                topic['action'], 'result' : result}, self.mac))
        return True

    @todict
    def err(self, topic, payload):
        '''
        Error from iCPE
        '''
        print('err')
        return

    def actlist(self, topic, payload):
        '''
        If Update is triggered to iCPE it will respond with list of ZWave
        NodeIDs connected to it, if not known we send query about that node
        '''
        known = [str(node.nodeid) for node in self.ZWaveNodes]
        print('known', known)
        ListFromiCPE = str(payload.decode('ascii')).split(',')
        for x in ListFromiCPE:
            if x in known or x == '1' or x == '0':
                pass
            else:
                outMQTTQueue.put(('icpe/0x' + self.mac + '/cmd/node/' + x +
                                  '/class/info/act/qry', ''))


    def actqry(self, topic, payload):
        '''
        information about a specific node, vendor id and such..
        Get's full information about capabilites from PepperDB
        '''
        known = [int(node.nodeid) for node in self.ZWaveNodes]
        if int(topic['nodeid']) in known or topic['nodeid'] == '0' or \
        topic['nodeid'] == '1':
            return
        iCPENode = iCPEModel.query.filter_by(mac = self.mac).first()
        payload = self.PayloadToDict(payload.decode('ascii'))
        ProductInfo = PepperDB.GetBaseInfo(payload['vid'], payload['ptype'],
                                           payload['pid'])
        AppendNode = NodeModel(topic['nodeid'], payload['vid'], payload['ptype'],
                                    payload['pid'], payload['generic_0'],
                                    ProductInfo['ProductName'],
                                    ProductInfo['BrandName'])
        iCPENode.znodes.append(AppendNode)
        db.session.add(iCPENode)
        db.session.commit()
        self.LoadNodes([AppendNode])
        return True

    def actset(self, topic, payload):
        node = self.__contains__(topic['nodeid'])
        print('actset', node)

    def actget(self, topic, payload):
        pass

    def actinclude(self, topic, payload):
        pass

    def actexclude(self, topic, payload):
        pass

