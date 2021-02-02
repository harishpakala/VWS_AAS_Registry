'''
Copyright (c) 2021-2022 OVGU LIA
Author: Harish Kumar Pakala
This source code is licensed under the Apache License 2.0 (see LICENSE.txt).
This source code may use other Open Source software components (see LICENSE.txt).
'''

import json
import logging
import os
import requests
import threading

from flask import Flask
from flask_restful import  Api,Resource,request

try:
    from utils.i40data import Generic
except ImportError:
    from main.utils.i40data import Generic

try:
    from abstract.endpointhandler import AASEndPointHandler
except ImportError:
    from main.abstract.endpointhandler import AASEndPointHandler

try:
    from aasendpointhandlers.rstapi_endpointresources import AAS,AASSubmodelbyId,AASSubModels,RetrieveMessage,AASDescbyId,AASSubModelDescAASId,AASSubModelDescbyId,AASDesc
except ImportError:
    from main.aasendpointhandlers.rstapi_endpointresources import AAS,AASSubmodelbyId,AASSubModels,RetrieveMessage,AASDescbyId,AASSubModelDescAASId,AASSubModelDescbyId,AASDesc

drv_rst_app = Flask(__name__)
drv_rst_app.secret_key = os.urandom(24)
drv_rst_api = Api(drv_rst_app)
drv_rst_app.logger.disabled = True
log = logging.getLogger('Python AAS Rest API')
log.setLevel(logging.ERROR)
log.disabled = True

    
class AASEndPointHandler(AASEndPointHandler):
    
    def __init__(self, pyAAS,msgHandler):
        self.pyAAS = pyAAS
        
        self.msgHandler = msgHandler
        
    def configure(self):
        
        self.ipaddressComdrv = '0.0.0.0'
        self.portComdrv = self.pyAAS.lia_env_variable["LIA_AAS_RESTAPI_PORT_INTERN"]
        
        # REST API
        drv_rst_api.add_resource(AAS, "/aas/<aasId>", resource_class_args=tuple([self.pyAAS]))
        drv_rst_api.add_resource(AASSubModels, "/aas/<aasId>/submodels", resource_class_args=tuple([self.pyAAS]))
        drv_rst_api.add_resource(AASSubmodelbyId, "/aas/<aasId>/submodels/<submodelId>", resource_class_args=tuple([self.pyAAS]))   
        
        # Resgitry API

        drv_rst_api.add_resource(AASDesc, "/api/v1/registry", resource_class_args=tuple([self.pyAAS]))
        drv_rst_api.add_resource(AASDescbyId, "/api/v1/registry/<aasId>", resource_class_args=tuple([self.pyAAS]))
        drv_rst_api.add_resource(AASSubModelDescbyId, "/api/v1/registry/<aasId>/submodels/<submodelId>", resource_class_args=tuple([self.pyAAS]))   
        drv_rst_api.add_resource(AASSubModelDescAASId, "/api/v1/registry/<aasId>/submodels", resource_class_args=tuple([self.pyAAS]))
        
        
        self.pyAAS.serviceLogger.info("REST API namespaces are configured")
                
    def update(self, channel):
        pass
    
    def run(self):
        drv_rst_app.run(host=self.ipaddressComdrv, port=self.portComdrv)
        self.pyAAS.serviceLogger.info("REST API namespaces are started")
    
    def start(self, pyAAS, uID):
        restServerThread = threading.Thread(target=self.run)
        restServerThread.start()

    def stop(self):
        self.pyAAS.serviceLogger.info("REST API namespaces are stopped.")
    
    def dispatchMessage(self, send_Message): 
        try:
            if (send_Message["frame"]["type"] == "register"):
                registryURL = self.pyAAS.registryAPI
                registryHeader = {"content-type": "application/json"}
                r = requests.put(registryURL, data=json.dumps(send_Message), headers=registryHeader)
                data = json.loads(r.text)
                self.msgHandler.putIbMessage(data)
            else:
                pass # Need to write the logic for dispatch of messages for other flows.
        except Exception as e:
            self.pyAAS.serviceLogger.info("Unable to publish the message to the target http server", str(e))
            self.sendExceptionMessageBack(str(e))
    
    def sendExceptionMessageBack(self,ErrorMessage):
        I40FrameData = {
                                "semanticProtocol": "Register",
                                "type" : "registerAck",
                                "messageId" : "registerAck_1",
                                "SenderAASID" : self.pyAAS.AASID,
                                "SenderRolename" : "HTTP_ENDPoint",
                                "conversationId" : "AASNetworkedBidding",
                                "replyBy" :  "",
                                "replyTo" :  "",                                
                                "ReceiverAASID" :  self.pyAAS.AASID,
                                "ReceiverRolename" : "Register"
                        }
        self.gen = Generic()
        self.frame = self.gen.createFrame(I40FrameData)
        
        self.InElem = self.pyAAS.dba.getAAsSubmodelsbyId(self.pyAAS.AASID,"StatusResponse")["message"][0]
        
        self.InElem["submodelElements"][0]["value"] = "E"
        self.InElem["submodelElements"][1]["value"] = "E009. delivery-error"
        self.InElem["submodelElements"][2]["value"] = ErrorMessage
         
        registerAckMessage ={"frame": self.frame,
                                "interactionElements":[self.InElem]}
        
        self.pyAAS.msgHandler.putIbMessage(registerAckMessage)
        
    
    def retrieveMessage(self, testMesage):  # todo
        pass
