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
import uuid

try:
    from abstract.endpointhandler import AASEndPointHandler
except ImportError:
    from main.abstract.endpointhandler import AASEndPointHandler

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish


class AASEndPointHandler(AASEndPointHandler):
    
    def __init__(self, pyAAS, msgHandler):
        self.pyAAS = pyAAS
        self.topicname = pyAAS.AASID
        self.msgHandler = msgHandler
    
    def on_connect(self, client, userdata, flags, rc):
        self.pyAAS.serviceLogger.info("MQTT channels are succesfully connected.")
        
    def configure(self):
        self.ipaddressComdrv = self.pyAAS.lia_env_variable["LIA_AAS_MQTT_HOST"]
        self.portComdrv = int(self.pyAAS.lia_env_variable["LIA_AAS_MQTT_PORT"])
        
        self.client = mqtt.Client(client_id=str(uuid.uuid4()))
        self.client.on_connect = self.on_connect
        self.client.on_message = self.retrieveMessage
        
        self.clientB = mqtt.Client(client_id=str(uuid.uuid4()))
        self.clientB.on_connect = self.on_connect
        self.clientB.on_message = self.retrieveMessage
        self.pyAAS.serviceLogger.info("MQTT channels are configured")
        
    def update(self, channel):
        self.client.subscribe(channel)
        self.client.loop_forever()
    
    def updateB(self, channel):
        self.clientB.subscribe(channel)
        self.clientB.loop_forever()
        
    def start(self, pyAAS, tpn):
        self.pyAAS = pyAAS
        self.tpn = tpn
        try :
            self.client.connect(self.ipaddressComdrv, port=(self.portComdrv))
            mqttClientThread1 = threading.Thread(target=self.update, args=(self.tpn,))
            mqttClientThread1.start()
          
        except Exception as e:
            self.pyAAS.serviceLogger.info('Unable to connect to the mqtt server ' + str(e))
            os._exit(0)
        try:
            self.clientB.connect(self.ipaddressComdrv, port=(self.portComdrv))
            mqttClientThread2 = threading.Thread(target=self.updateB, args=("BT1",))
            mqttClientThread2.start()
        except Exception as e:
            self.pyAAS.serviceLogger.info('Unable to connect to the mqtt server ' + str(e))
            os._exit(0)
        self.pyAAS.serviceLogger.info("MQTT channels are started")
            

    def stop(self):
        try: 
            self.client.loop_stop(force=False)
            self.client.disconnect()
            
        except Exception as e:
            self.pyAAS.serviceLogger.info('Error disconnecting to the server ' + str(e))
        
        try: 
            self.clientB.loop_stop(force=False)
            self.clientB.disconnect()
            
        except Exception as e:
            self.pyAAS.serviceLogger.info('Error disconnecting to the server ' + str(e))

    def dispatchMessage(self, send_Message): 
        publishTopic = self.pyAAS.BroadCastMQTTTopic
        try:
            publishTopic = send_Message["frame"]["receiver"]["identification"]["id"]
        except Exception as E:
            pass
        try:
            if (publishTopic == self.pyAAS.AASID):
                self.msgHandler.putIbMessage(send_Message)
            else:
                self.client.publish(publishTopic, str(json.dumps(send_Message)))
                self.pyAAS.serviceLogger.info("A new message is publish to "+ publishTopic)
        except Exception as e:
            self.pyAAS.serviceLogger.info("Unable to publish the message to the mqtt server", str(e))
            
    def retrieveMessage(self, client, userdata, msg):
        msg1 = str(msg.payload, "utf-8")
        jsonMessage = json.loads(msg1)      
        try:
            if (jsonMessage["frame"]["sender"]["identification"]["id"] == self.pyAAS.AASID):
                self.msgHandler.putIbMessage(jsonMessage)
            else:
                self.msgHandler.putIbMessage(jsonMessage)
                self.pyAAS.serviceLogger.info("A new Message received from the sender " + jsonMessage["frame"]["receiver"]["identification"]["id"])
        except:
            pass
            
