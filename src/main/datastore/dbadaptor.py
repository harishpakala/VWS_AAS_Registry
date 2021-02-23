'''
Copyright (c) 2021-2022 OVGU LIA
Author: Harish Kumar Pakala
This source code is licensed under the Apache License 2.0 (see LICENSE.txt).
This source code may use other Open Source software components (see LICENSE.txt).
'''

import pymongo
import json
try:
    from utils.utils import HTTPEndpointObject
except ImportError:
    from main.utils.utils import HTTPEndpointObject

class DB_ADAPTOR(object):
    '''
    classdocs
    '''

    def __init__(self,pyAAS):
        '''
        Constructor
        '''
        self.pyAAS = pyAAS
        self.db_host = self.pyAAS.lia_env_variable['LIA_MONGO_HOST']
        self.db_port = self.pyAAS.lia_env_variable['LIA_MONGO_PORT']
        self.mongoclient = pymongo.MongoClient("mongodb://"+self.db_host+":"+self.db_port+"/")
        
        self.mongodb = self.mongoclient["AASXRegistry_"+self.pyAAS.AASID]
        self.mongocol_aas = self.mongodb["aas_"+self.pyAAS.AASID]
        self.mongocol_Messages = self.mongodb["messages_"+self.pyAAS.AASID]
        self.mongocol_aasDesc = self.mongodb["aasDesc"+self.pyAAS.AASID]
        self.mongocol_aasDescEndPoint = self.mongodb["aasDescEndPoint"+self.pyAAS.AASID]
        
## AAS related Entries
    def getAAS(self,data):
        returnMessageDict = {}
        resultList = []

        try:
            AAS = self.mongocol_aas.find({ 
                                        "assetAdministrationShells.0.idShort" : data["aasId"]
                                    },
                                    { 
                                        "_id" : 0.0
                                    })
            for aas in AAS:
                resultList.append(aas)

            if len(resultList) == 0:
                returnMessageDict = {"message":["No Asset Administration Shell with passed id found"],"status":404}
            else :
                returnMessageDict = {"message": resultList,"status":200}
            
        except Exception as E:
            print(str(E))
            returnMessageDict = {"message": ["Unexpected Internal Server Error"],"status":500}
        return returnMessageDict
    
    def deleteAASByID(self,data):
        aasId = data["aasId"]
        returnMessageDict = {}
        try:
            deleteResult = self.mongocol_aas.remove({ 
                                    "assetAdministrationShells.0.idShort" : aasId
                                                })
            if (deleteResult["n"] == 0):
                returnMessageDict = {"message" : ["No Asset Administration Shell with passed id found"], "status": 404}
            else:
                returnMessageDict = {"message" : ["The Asset Administration Shell was deleted successfully"], "status": 200}            
        except Exception as E:
            returnMessageDict = {"message": ["Unexpected Internal Server Error"],"status":500}
        return returnMessageDict
    
    def putAAS(self,data):
        returnMessageDict = {}
        aas = data["updateData"]
        try:
            response = self.deleteAASByID(data)
            if (response["status"] == 200):
                self.mongocol_aas.insert_one(aas)
                returnMessageDict = {"message" : ["The Asset Administration Shell's registration was successfully renewed"],"status":200}
            elif(response["status"] == 404):
                self.mongocol_aas.insert_one(aas)
                returnMessageDict = {"message" : ["The Asset Administration Shell's registration was successfull"],"status":200}
            else:
                returnMessageDict = response
        except Exception as E:
            returnMessageDict = {"message": ["Unexpected Internal Server Error"],"status":500}
        return returnMessageDict
    
    def getSubmodels(self,data):
        returnMessageDict = {}
        resultList = []

        try:
            aasSubmodels = self.mongocol_aas.find({ 
                                    "assetAdministrationShells.0.idShort" : data["aasId"]
                                    }, 
                                    { 
                                        "submodels" : 1.0,
                                        "_id" : 0.0
                                    })
            for aas in aasSubmodels:
                for submodel in aas["submodels"]:
                    resultList.append(submodel)

            if len(resultList) == 0:
                returnMessageDict = {"message":["No Asset Administration Shell with passed id found"],"status":404}
            else :
                returnMessageDict = {"message": [{"submodels":resultList}],"status":200}
                
        except Exception as E:
            returnMessageDict = {"message": ["Unexpected Internal Server Error"],"status":500}
                
        return returnMessageDict
            
    def getSubmodelsbyId(self,data):
        returnMessageDict = {}
        resultList = []
        resultListTemp = []
        aasId = data["aasId"]
        submodelId = data["submodelId"]
        try:
            aasSubmodels = self.mongocol_aas.find({
                                        "assetAdministrationShells.0.idShort": aasId, 
                                    }, 
                                    { 
                                        "submodels" : 1.0,
                                        "_id" : 0.0
                                    }
                                    )
            
            for aas in aasSubmodels:
                for submodel in aas["submodels"]:
                    resultListTemp.append(submodel)

            if len(resultListTemp) == 0:
                returnMessageDict = {"message":["No Asset Administration Shell with passed id found"],"status":404}
                
            else :
                for submodel in resultListTemp:
                    if submodel["idShort"] == submodelId:
                        resultList.append(submodel)
                if len(resultList) == 0:
                    returnMessageDict = {"message":["No submodel with the passed id found"],"status":404}
                else:
                    returnMessageDict = {"message": resultList,"status":200}
                
        except Exception as E:
            returnMessageDict = {"message": ["Unexpected Internal Server Error"],"status":500}
        return returnMessageDict
    
    def putSubmodels(self,data):
        returnMessageDict = {}
        submodelData = data["updateData"]
        aasId = data["aasId"]
        submodels = submodelData
        try:
            response1 = self.getAAS(data)
            if (response1["status"] == 200):
                for submodel in submodels["submodels"]:
                    response2 = self.deleteSubmodelsbyId({"updateData":"emptyData","aasId":aasId,"submodelId":submodel["idShort"]})
                    if (response2["status"] == 500):
                        return response2
                    else:
                        pass
                aasData = self.getAAS(data)["message"][0]
                for submodel in submodels["submodels"]:
                    aasData["submodels"].append(submodel)
                    keys ={
                            "keys": [
                                        {
                                            "type": "Submodel",
                                            "local": True,
                                            "value": submodel["identification"]["id"],
                                            "index": 0,
                                            "idType": submodel["identification"]["idType"]
                                        }
                                    ]
                            }
                    aasData["assetAdministrationShells"][0]["submodels"].append(keys) 
                response3 = self.putAAS({"updateData":aasData,"aasId":aasId})
                if (response3["status"] == 200):
                    if (response2["status"] == 200):
                        returnMessageDict = {"message" : ["The Submodels are renewed successfully"],"status":200}
                    elif (response2["status"] == 404):
                        returnMessageDict = {"message" : ["The Submodels are created successfully"],"status":200}
                    else :
                        returnMessageDict = response2
                else :
                    returnMessageDict = response3
            else:
                returnMessageDict = response1
        except Exception as e:
            returnMessageDict = {"message" : ["Unexpected Internal Server Error"], "status":500}
        return returnMessageDict        
    
    def deleteSubmodelsbyId(self,data):
        returnMessageDict = {}
        submodelId = data["submodelId"]
        try:
            response = self.getAAS(data)
            if (response["status"] == 200):
                aasData = response["message"][0]
                i = 0
                present = False
                for submodel in response["message"][0]["submodels"]:
                    if (submodel["idShort"] == submodelId):
                        del aasData["submodels"][i]
                        j = 0
                        present = True 
                        for submodelAAS in response["message"][0]["assetAdministrationShells"][0]["submodels"]:
                            for key in submodelAAS["keys"]:
                                if (key["value"] == submodel["identification"]["id"]):
                                    del aasData["assetAdministrationShells"][0]["submodels"][j]
                            j = j + 1
                    i = i + 1
                if (present):
                    response2 = self.putAAS({"updateData":aasData,"aasId":data["aasId"]})
                    if (response2["status"] == 200):
                        return {"message" : ["The Submodels deleted successfully"],"status":200}
                    else :
                        return response2
                else:
                    return {"message" : ["No Submodel with the passed Id found"],"status":404} 
            else:
                returnMessageDict = response
        except Exception as E:
            returnMessageDict = {"message" : ["Unexpected Internal Server Error"], "status":500}
        return returnMessageDict        

## Message Level Entries

    def saveSkillMessage(self,skillMessage,messageType):
        returnMessageDict = {}
        self.mongocol_messageType = self.mongodb[messageType]
        try:
            self.mongocol_messageType.insert_one(skillMessage)
            returnMessageDict = {"message": ["The details are successfully recorded"],"status":200}
        except Exception as E:
            returnMessageDict = {"message": ["Unexpected Internal Error"],"status":500}
        return returnMessageDict  
    
    def checkforConversationDbExistence(self):
        returnMessageDict = {}
        try:
            resultList = self.mongocol_Messages.find({'coversationId': "AAS_Orders"})
            returnMessageDict = {"message": [int(resultList.count())],"status":200}
        except Exception as e:
            returnMessageDict = {"message": ["Unexpected Internal Error"],"status":500}
        return returnMessageDict
    
    def createConversationDataBase(self):
        returnMessageDict = {}
        message = self.checkforConversationDbExistence()
        if (message["status"] == 200):
            if (message["message"] > 0):
                returnMessageDict = {"message": ["Data Already Exisiting."],"status":200}                
                return returnMessageDict
            else:
                return self._createConversationDataBase()
        else :
            returnMessageDict = {"message": ["Unexpected Internal Error"],"status":500}
        
    def _createConversationDataBase(self):
        returnMessageDict = {}
        baseConversation = {
                    "coversationId":"AAS_Orders", 
                    "messages":   [
                                        {
                                            "messageType" :"Order",
                                            "message_Id" :"OrderId_123",
                                            "message" :{
                                                "frame":  {},
                                                "interactionElements":{}
                                                }
                                        }
                                    ]
                    }
        try:
            self.mongocol_Messages.insert_one(baseConversation)
            returnMessageDict = {"message": ["The conversation database is setup "],"status":200}            
        except Exception as E:
            returnMessageDict = {"message": ["Unexpected Internal Error"],"status":500}
        return returnMessageDict
    
    def createNewConversation(self,coversationId):
        returnMessageDict = {}
        coversationId = coversationId
        newConversation = {
                "coversationId":coversationId, 
                "messages":   []
            }
        try:
            self.mongocol_Messages.insert_one(newConversation)
            returnMessageDict = {"message": ["The details are successfully recorded"],"status":200}            
        except Exception as E:
            returnMessageDict = {"message": ["Unexpected Internal Error"],"status":500}
        return returnMessageDict
    
    def saveNewConversationMessage(self,coversationId,messageType,messageId,message):
        message = {
                    "messageType" :messageType,
                    "message_Id" :messageId,
                    "message" :message
                }
        returnMessageDict = {}
        try:
            self.mongocol_Messages.update_one({'coversationId': coversationId},
                                              {"$push": {"messages": message}})
            returnMessageDict = {"message": ["The details are successfully recorded"],"status":200}            
        except Exception as E:
            returnMessageDict = {"message": ["Unexpected Internal Error"],"status":500}
        return returnMessageDict    

    def getConversationCount(self):
        returnMessageDict = {}
        try:
            result = int(self.mongocol_Messages.find().count())
            returnMessageDict = {"message": [result],"status":200}            
        except Exception as E:
            returnMessageDict = {"message": ["Unexpected Internal Error"],"status":500}
        return returnMessageDict  
    
    def getConversationsById(self,coversationId):
        returnMessageDict = {}
        try:
            resultList = []
            message = self.mongocol_Messages.find({'coversationId': coversationId})
            for mg in message:
                resultList.append(mg) 
            if len(resultList) > 0: 
                returnMessageDict = {"message": resultList,"status":200}
            else:
                returnMessageDict = {"message": ["No conversation found"],"status":404}                
        except Exception as e:
            returnMessageDict = {"message": ["Unexpected Internal Error"],"status":500}
        return returnMessageDict    
    
    def getMessagebyId(self,messageId,conversationId,messageType):
        try:
            messagesList = self.mongocol_Messages.find({'coversationId': conversationId})
            for message in messagesList:
                for mg in message["messages"]:
                    if (mg["message_Id"] == messageId):
                        returnMessageDict = {"message": [mg["message"]],"status":200}
        except Exception as e:
            returnMessageDict = {"message": ["Unexpected Internal Error"],"status":500}
        return returnMessageDict 
            
    def getMessageCount(self):
        count = 0
        try:
            messagesList = self.mongocol_Messages.find()
            for message in messagesList:
                count = count + len (message["messages"])
            returnMessageDict = {"message": [count],"status":200}
        except Exception as e:
            returnMessageDict = {"message": ["Unexpected Internal Error"],"status":500}
        return returnMessageDict 

    def getAAsSubmodelsbyId(self,aasId,submodelId):
        if (submodelId == "StatusResponse"):
            return {"message":[self.pyAAS.aasConfigurer.submodel_statusResponse_path],"status":200}
        
        returnMessageDict = {}
        resultList = []
        resultListTemp = []

        try:
            aasSubmodels = self.mongocol_aas.find({
                                        "assetAdministrationShells.0.idShort": aasId, 
                                    }, 
                                    { 
                                        "submodels" : 1.0,
                                        "_id" : 0.0
                                    }
                                    )
            
            for aas in aasSubmodels:
                for submodel in aas["submodels"]:
                    resultListTemp.append(submodel)

            if len(resultListTemp) == 0:
                message = []
                message.append("E007. internal-error")
                message.append("Currently no AAS with the given ID has registered with the registry")
                returnMessageDict = {"message":message,"status":400}
                
            else :
                for submodel in resultListTemp:
                    if submodel["idShort"] == submodelId:
                        resultList.append(submodel)
                if len(resultList) == 0:
                    message = []
                    message.append("E007. internal-error")
                    message.append("The AAS does not contain the specified submodel")
                    returnMessageDict = {"message":message,"status":400}
                else:
                    returnMessageDict = {"message": resultList,"status":200}
                
        except Exception as E:
            returnMessageDict = {"message": ["Unexpected Internal Error"],"status":500}
        return returnMessageDict 

    def getAASDescByID(self,data):
        returnMessageDict = {}
        resultList = []
        try:
            AAS = self.mongocol_aasDesc.find({ 
                                                "aasId" : data["aasId"]
                                            },
                                            { 
                                                "_id" : 0.0
                                            })
            for aas in AAS:
                resultList.append(aas["data"])

            if len(resultList) == 0:
                returnMessageDict = {"message":["No Asset Administration Shell with passed id found"],"status":404}
            else :
                returnMessageDict = {"message": resultList,"status":200}

        except Exception as E:
            returnMessageDict = {"message": ["Unexpected Internal Server Error"],"status":500}
        return returnMessageDict

    def deleteAASDescById(self,data):
        returnMessageDict = {}
        aasId = data["aasId"]
        try:
            deleteResult = self.mongocol_aasDesc.remove({ 
                                                        "aasId" : aasId
                                                    })
            if (deleteResult["n"] == 0):
                returnMessageDict = {"message" : ["No Asset Administration Shell Descriptor with passed id found"], "status": 404}
            else:
                returnMessageDict = {"message" : ["The Asset Administration Shell Descriptor was deleted successfully"], "status": 200}
        except Exception as E:
            returnMessageDict = {"message" : ["Unexpected Internal Server Error"], "status":500}
        return returnMessageDict
     
    def putAASDescByID(self,data):
        returnMessageDict = {}
        descData = data["updateData"]
        aasId = data["aasId"]
        try:
            response = self.deleteAASDescById(data)
            heo = HTTPEndpointObject(self.pyAAS)
            if (response["status"] == 200):
                self.mongocol_aasDesc.insert_one({ "aasId" : aasId,"data":descData})
                heo.insert(descData)
                returnMessageDict = {"message" : ["The Asset Administration Shell's registration was successfully renewed"],"status":200}
            elif(response["status"] == 404):
                self.mongocol_aasDesc.insert_one({  "aasId" : aasId,"data":descData})
                heo.insert(descData)
                returnMessageDict = {"message" : ["The Asset Administration Shell's registration was successfull"],"status":200}
            else:
                returnMessageDict = response
        except Exception as E:
            print(str(E))
            returnMessageDict = {"message": ["Unexpected Internal Server Error"],"status":500}
        return returnMessageDict
 
    def getSubmodelDescByID(self,data):
        returnMessageDict = {}
        aasId = data["aasId"]
        submodelId =data["submodelId"]
        try:
            response = self.getAASDescByID(data)
            if (response["status"] == 200):
                present = False
                for submodelDesc in response["message"][0]["submodelDescriptors"]:
                    if submodelDesc["idShort"] == submodelId:
                        returnMessageDict = {"message" : [submodelDesc], "status": 200}
                        present = True
                if (not present):
                    returnMessageDict = {"message" : ["Submodel with passed id not found"], "status": 404}
            else:
                returnMessageDict = response
        except Exception as e:
            returnMessageDict = {"message" : ["Unexpected Internal Server Error"], "status":500}
        return returnMessageDict

    def putSubmodelDescByID(self,data):
        try:
            returnMessageDict = {}
            aasId = data["aasId"]
            submodelId = data["submodelId"]
            descData = data["updateData"]
            response1 = self.getSubmodelDescByID(data)
            if (response1["status"] == 200):
                response2 = self.deleteSubmodelDescByID(data)
                if (response2["status"] == 200):
                    response3 = self.getAASDescByID(data) 
                    if (response3["status"] == 200):
                        data = response3["message"][0]
                        data["submodelDescriptors"].append(descData)
                        response4 = self.putAASDescByID({"aasId":aasId,"updateData":data})
                        if (response4["status"] == 200):
                            returnMessageDict = {"message" : ["The Submodel descriptor was successfully renewed"],"status":200}
                        else :
                            returnMessageDict = response4
                    else:
                        returnMessageDict = response3
                else:
                    returnMessageDict = response2
            else:
                response5 = self.getAASDescByID(data) 
                if (response5["status"] == 200):
                    data = response5["message"][0]
                    data["submodelDescriptors"].append(descData)
                    response6 = self.putAASDescByID({"aasId":aasId,"updateData":data})
                    if (response6["status"] == 200):
                        returnMessageDict = {"message" : ["The Submodel descriptor was created successfully."],"status":200}
                    else :
                        returnMessageDict = response6
        except Exception as E:
            returnMessageDict = {"message" : ["Unexpected Internal Server Error"], "status":500}
        return returnMessageDict

    def deleteSubmodelDescByID(self,data):
        returnMessageDict = {}
        aasId = data["aasId"]
        submodelId = data["submodelId"]
        try:
            response = self.getAASDescByID(data)
            if (response["status"] == 200):
                aasDescData = response["message"][0]
                aasSubmodelDescData = response["message"][0]["submodelDescriptors"]
                i = 0
                present = False
                for submodelDesc in response["message"][0]["submodelDescriptors"]:
                    if submodelDesc["idShort"] == submodelId:
                        del aasSubmodelDescData[i]
                        present = True
                        break
                    i = i + 1
                if (not present):
                    returnMessageDict = {"message" : ["Submodel Descriptor with passed id not found"], "status": 404}
                else:
                    aasDescData["submodelDescriptors"] = aasSubmodelDescData
                    response2 = self.putAASDescByID({"aasId":aasId, "updateData" :aasDescData})
                    if response["status"] == 200:
                        returnMessageDict = {"message" : ["The Submodel Descriptor was successfully unregistered"], "status": 200}
                    else:
                        returnMessageDict = response
            else:
                returnMessageDict = response
        except Exception as e:
            returnMessageDict = {"message" : ["Unexpected Internal Server Error"], "status":500}
        return returnMessageDict    
    
    def insertDescriptorEndPoint(self,data):
        self.mongocol_aasDescEndPoint.insert_one(data)
    
    def deleteDescriptorEndPoint(self,aasId):
        deleteResult = self.mongocol_aasDescEndPoint.remove({ 
                                    "aasId" : aasId
                                                })
        
    def getDescriptorEndPoint(self):
        returnMessageDict = {}
        resultList = []
        try:
            AAS = self.mongocol_aasDescEndPoint.find({},
                                            { 
                                                "_id" : 0.0
                                            })
            
            for aasD in AAS:
                resultList.append(aasD)
            returnMessageDict = {"message": resultList,"status":200}

        except Exception as E:
            returnMessageDict = {"message" : ["Unexpected Internal Server Error"], "status":500}
        return returnMessageDict        
        
    def getAllDesc(self,data):
        returnMessageDict = {}
        resultList = []
        try:
            AAS = self.mongocol_aasDesc.find({},
                                            { 
                                                "_id" : 0.0
                                            })
            
            for aas in AAS:
                resultList.append(aas["data"])

            if len(resultList) == 0:
                returnMessageDict = {"message":["No Asset Administration Shell descriptors are yet registered"],"status":404}
            else :
                resultDict = {}
                i = 0
                for result in resultList:
                    resultDict[i] = result
                    i = i + 1
                returnMessageDict = {"message": [resultDict],"status":200}

        except Exception as E:
            returnMessageDict = {"message" : ["Unexpected Internal Server Error"], "status":500}
        return returnMessageDict

    def getSubmodelDescByAASId(self,data):
        returnMessageDict = {}
        resultList = []
        try:
            AAS = self.mongocol_aasDesc.find({ 
                                                "aasId" : data["aasId"]
                                            },
                                            { 
                                                "_id" : 0.0
                                            })
            i = 0 
            for aas in AAS:
                i = i + 1
                for submodeDesc in (aas["data"]["submodelDescriptors"]):
                    resultList.append(submodeDesc)
            if (i == 0):
                returnMessageDict = {"message":["No Asset Administration Shell descriptors are yet registered"],"status":404}
            else:
                if len(resultList) == 0:
                    returnMessageDict = {"message":["The Asset Administration Shell Descriptors does not have any submodel descriptors"],"status":404}
                else :
                    returnMessageDict = {"message" : [{"submodelDescriptors":resultList}], "status":200}

        except Exception as E:
            returnMessageDict = {"message" : ["Unexpected Internal Server Error"], "status":500}
        return returnMessageDict  
       


   
if __name__ == "__main__":
    dba = DB_ADAPTOR()
    dba.getAAS()
    