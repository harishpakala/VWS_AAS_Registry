'''
Copyright (c) 2021-2022 OVGU LIA
Author: Harish Kumar Pakala
This source code is licensed under the Apache License 2.0 (see LICENSE.txt).
This source code may use other Open Source software components (see LICENSE.txt).
'''

import  threading
import time
import uuid

try:
    import queue as Queue
except ImportError:
    import Queue as Queue 

try:
    from datastore.datamanager import DataManager
except ImportError:
    from main.datastore.datamanager import DataManager

try:
    from utils.aaslog import serviceLogHandler,LogList
except ImportError:
    from main.utils.aaslog import serviceLogHandler,LogList


class MessageHandler(object):
    '''
    classdocs
    '''

    def __init__(self, pyAAS):
        '''
        Constructor
        '''
        self.pyAAS = pyAAS
        self.inBoundQueue = Queue.Queue()
        self.outBoundQueue = Queue.Queue()
        
        self.transportQueue = Queue.Queue()
        self.transportP1Queue = Queue.Queue()
        self.transportP2Queue = Queue.Queue()
        
        self.RegistryHandlerLogList = LogList()
        self.RegistryHandlerLogList.setMaxSize(maxSize= 200)

        
        self.logListDict = {
                              "RegistryHandler" : self.RegistryHandlerLogList
                            }
        
        self.POLL = True
        
    def start(self, skillName, AASendPointHandlerObjects):
        self.skillName = skillName
        self.AASendPointHandlerObjects = AASendPointHandlerObjects
           
        while self.POLL:
            time.sleep(0.001)
            if (self.outBoundQueue).qsize() != 0:
                obThread = threading.Thread(target=self.sendOutBoundMessage, args=(self.getObMessage(),))     
                obThread.start()
            
            if (self.inBoundQueue).qsize() != 0:
                ibThread = threading.Thread(target=self._receiveMessage_, args=(self.getIbMessage(),))     
                ibThread.start()
            
            if (self.transportQueue).qsize() != 0:
                transportThread = threading.Thread(target=self.__sendTransportMessage_,args=(self.getTransportMessage(),))
                transportThread.start()
            
            if (self.transportP1Queue).qsize() != 0:
                transportP1Thread = threading.Thread(target=self.__sendTransportP1Message_,args=(self.getTransportP1Message(),))
                transportP1Thread.start()

            if (self.transportP2Queue).qsize() != 0:
                transportP2Thread = threading.Thread(target=self.__sendTransportP2Message_,args=(self.getTransportP2Message(),))
                transportP2Thread.start()
                                            
    def stop(self):
        self.POLL = False
        
    def putIbMessage(self, message):
        self.inBoundQueue.put((message))
    
    def getIbMessage(self):
        return self.inBoundQueue.get()
    
    def putObMessage(self, message):
        self.outBoundQueue.put(message)
    
    def getObMessage(self):
        return self.outBoundQueue.get()
    
    def getTransportMessage(self):
        return self.transportQueue.get()
    
    def putTransportMessage(self,message):
        self.transportQueue.put(message)
    
    def getTransportP1Message(self):
        return self.transportP1Queue.get()
    
    def putTransportP1Message(self,message):
        self.transportP1Queue.put(message)
    
    def getTransportP2Message(self):
        return self.transportP2Queue.get()
    
    def putTransportP2Message(self,message):
        self.transportP2Queue.put(message)
    
    def assigntoSkill(self, _skillName):
        return self.skillName[_skillName]
    
    def createNewUUID(self):
        return uuid.uuid4()
        
    def _receiveMessage_(self, jMessage):
        try:
            _skillName = jMessage["frame"]["receiver"]["role"]["name"]
            return self.assigntoSkill(_skillName).receiveMessage(jMessage)
        except:
            for skillName in self.skillName.keys():
                return self.assigntoSkill(skillName).receiveMessage(jMessage)

    def sendOutBoundMessage(self, ob_Message):
        try:
            adaptorType = ob_Message["frame"]["replyTo"]
            self.AASendPointHandlerObjects[adaptorType].dispatchMessage(ob_Message)
        except Exception as E:
            self.putIbMessage(ob_Message)
            
    
    def __sendTransportMessage_(self,oT_Message):
        try :
            targetResponse = self.AASendPointHandlerObjects["RESTAPI"].dispatchMessage(oT_Message)
            if targetResponse:
                pass
            else:
                time.sleep(2)
                self.putTransportP1Message(oT_Message)
        except Exception as E:
            time.sleep(2)
            self.putTransportP1Message(oT_Message)
 
    def __sendTransportP1Message_(self,oT_P1Message):
        try :
            targetResponseP1 = self.AASendPointHandlerObjects["RESTAPI"].dispatchMessage(oT_P1Message)
            if targetResponseP1:
                pass
            else:
                time.sleep(2)
                self.putTransportP2Message(oT_P1Message)
        except Exception as E:
            time.sleep(2)
            self.putTransportP2Message(oT_P1Message)       

    def __sendTransportP2Message_(self,oT_P2Message):
        try :
            targetResponseP2 = self.AASendPointHandlerObjects["RESTAPI"].dispatchMessage(oT_P2Message)
        except Exception as E:
            pass