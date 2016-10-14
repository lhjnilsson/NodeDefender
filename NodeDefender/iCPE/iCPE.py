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
from .. import db, handler, outMQTTQueue, inMQTTQueue,\
        outSocketQueue, NodeLogQueue
from ..models import iCPEModel, LocationModel, NodeModel, NodeClassModel,\
NodeHiddenFieldModel
import logging
from collections import namedtuple
from . import PepperDB
from ..mqtt import MQTT
from threading import Thread
from .ZWave import ZWaveNode
from functools import wraps
from datetime import datetime
from os import path
from .MQTTFunctions import MQTTFunctions
from .WSFunctions import WSFunctions

class iCPE(MQTTFunctions, WSFunctions):
    '''
    Controller of a single iCPE
    '''
    ZWaveNode = namedtuple('ZWaveNode', 'nodeid callback')
    def __init__(self, alias, mac, ZNodes):
        self.alias = alias
        self.mac = mac
        self.ZWaveNodes = set()
        self.LoadNodes(ZNodes)
        self.logger = logging.getLogger(self.alias)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(handler)
        self.logger.info('iCPE {} Started'.format(self.mac))

    @classmethod
    def FromDB(cls, SQLObject):
        '''
        Alternative constructor from SQL Object
        '''
        alias = SQLObject.alias
        mac = SQLObject.mac
        ZNodes = SQLObject.znodes
        return cls(alias, mac, ZNodes)
    
    def __get__(self, index):
        return self.ZWaveNodes[index]

    def __call__(self, topic, payload):
        getattr(self, topic[2])(topic, payload)

    def __contains__(self, nodeid):
        try:
            return [znode for znode in self.ZWaveNodes if int(znode.nodeid) ==
                    int(nodeid)][0]
        except IndexError:
            return False

    @staticmethod
    def PayloadToDict(payload):
        retdict = {}
        _list = str(payload).split(' ')
        for x in _list:
            y = x.split('=')
            try:
                retdict[y[0]] = y[1]
            except IndexError:
                pass
        return retdict

    def Form(self):
        return [znode.callback.Form() for znode in
    self.ZWaveNodes]

    def UpdateNodeInfo(self, **kwargs):
        Node = self.__contains__(kwargs['nodeid'])
        if Node:
            Node.callback.Update(**kwargs)
            return True
        else:
            return False

    def UpdateNode(self):
        try:
            outMQTTQueue.put(('icpe/0x' + self.mac +
                             '/cmd/node/0/class/node/act/list', ''))
        except Exception as e:
            self.logger.critical('Unable to publish on MQTT')

    def NodeInformation(self, mac, n):
        try:
            outMQTTQueue.put(('icpe/0x' + mac + '/cmd/node' + n +
                                    '/class/info/act/qry', ''))
        except Exception as e:
            self.logger.critical('Unable to publish MQTT')

    def NodeInclude(self):
        try:
            outMQTTQueue.put(('icpe/0x' + self.mac +
                                    '/cmd/node/0/class/mode/act/include', ''))
        except Exception as e:
            self.logger.critical('Unable to publish on MQTT')

    def NodeExclude(self):
        try:
            outMQTTQueue.put(('icpe/0x' + self.mac +
                                    '/cmd/node/0/class/mode/act/exclude', ''))
        except Exception as e:
            self.logger.critical('Unable to publish on MQTT')

    def LoadNodes(self, nodes):
        if len(nodes) < 1:
            return
        for node in nodes:
            kwargs = {}
            kwargs['Alias'] = node.alias
            kwargs['Brandname'] = node.brandname
            kwargs['Productname'] = node.productname
            kwargs['Generic Class'] = node.generic_class
            self.LoadNode(node, **kwargs)

    def LoadNode(self, nodemodel, **kwargs):
        NodeClass, unsupported = ZWaveNode(self.mac, nodemodel.nodeid,
                                           nodemodel.nodeclasses)
        kwargs['unsupported'] = unsupported
        NodeObj = NodeClass(self.mac, nodemodel.nodeid, outMQTTQueue, outSocketQueue, **kwargs)
        self.ZWaveNodes.add(self.ZWaveNode(nodemodel.nodeid, NodeObj))
        return True

    def AddNode(self, nodeid, vid, ptype, pid, generic_0):
        iCPENode = iCPEModel.query.filter_by(mac = self.mac).first()
        ProdInfo = PepperDB.GetBaseInfo(vid, ptype, pid)
        AddNode = NodeModel(nodeid, vid, ptype, pid, generic_0,
                            ProdInfo['ProductName'], ProdInfo['BrandName'])
        AddNode = self.AddNodeClasses(AddNode, vid, ptype, pid)
        iCPENode.znodes.append(AddNode)
        db.session.add(iCPENode)
        db.session.commit()
        self.LoadNodes([AddNode])
        return True

    def AddNodeClasses(self, nodemodel, vid, ptype, pid):
        classlist = PepperDB.Classlist(vid, ptype, pid)
        print('classlist', classlist)
        for cls in classlist:
            print('adding ', cls)
            nodemodel.nodeclasses.append(NodeClassModel(cls))
        return nodemodel

    def removenode(self):
        pass

class iCPEset:
    '''
    set of iCPE class- objects
    '''
    iCPE = namedtuple('iCPE', 'mac online callback')
    def __init__(self, icpes):
        self.iCPEs = set()
        self.LoadiCPEs(icpes)
        _t1 = Thread(target=self._MQTTSubscriber).start()

    @classmethod
    def FromDB(cls):
        '''
        Alternative constructor to load from SQL
        '''
        icpes = iCPEModel.query.all()
        if not icpes:
            pass # Logg in future...
        return cls(icpes)

    def __get__(self, index):
        return self.iCPEs[index]

    def __iter__(self):
        return iter(self.iCPEs)

    def __len__(self):
        return len(self.iCPEs)

    def __contains__(self, mac):
        try:
            return [icpe for icpe in self.iCPEs if mac == icpe.mac][0]
        except IndexError:
            return False

    def __call__(self, mac, topic, payload):
        icpe = self.__contains__(mac)
        if icpe:
            icpe.callback(topic, payload)
            return True
        else:
            return False

    def WebForm(self, mac):
        icpe = self.__contains__(mac)
        if not icpe:
            return False
        return icpe.callback.Form()

    def UpdateNodeInfo(self, **kwargs):
        icpe = self.__contains__(kwargs['mac'])
        if not icpe:
            return False
        return icpe.callback.UpdateNodeInfo(**kwargs)

    def _MQTTSubscriber(self):
        while True:
            mac, topic, payload = inMQTTQueue.get()
            icpe = [icpe for icpe in self.iCPEs if mac == icpe.mac][0]
            if icpe:
                icpe.callback(topic, paylod)

    def LoadiCPEs(self, icpes):
        for icpe in icpes:
            self.iCPEs.add(self.iCPE(icpe.mac, False, iCPE.FromDB(icpe)))
        else:
            return None
        return len(icpes)


    def AddiCPE(self, mac, alias, street, city):
        if len(mac) != 12:
            raise ValueError('MAC needs to be 12 digits')
        newiCPE = iCPEModel(mac.upper(), alias)
        location = LocationModel(street, city)
        newiCPE.location = location
        db.session.add(newiCPE)
        db.session.commit()
        self.iCPEs.add(self.iCPE(mac.upper(), False, iCPE.FromDB(newiCPE)))
        return True

    def DeleteiCPE(self, mac):
        icpe = self.__contains__(mac)
        if not icpe:
            raise TypeError('not a known iCPE')
        node = iCPEModel.query.filter_by(mac = mac).first()
        if not node:
            raise ValueError('Mac is not registered')
        db.session.delete(node)
        db.session.commit()
        self.iCPEs.remove(icpe)
        return True

    def Event(self, mac, event):
        icpe = self.__contains__(mac)
        if not icpe:
            return False
        getattr(icpe.callback, event)()

    def SocketEvent(self, **kwargs):
        icpe = self.__contains__(kwargs['mac'])
        if not icpe:
            return False
        icpe.callback.SocketEvent(**kwargs)

if not path.isfile('NodeDefender/iCPE/PepperDB/last_changed.txt'):
    print('--PepperDB not intialized, downloading..')
    PepperDB.DownloadDB()
    print('--PepperDB Complete')

