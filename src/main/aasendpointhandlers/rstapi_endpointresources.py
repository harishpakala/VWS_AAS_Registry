'''
Created on 21.05.2020

@author: pakala
'''
import json
import requests

from flask_restful import Resource,request
from flask import render_template,Response,redirect,flash,make_response
from jsonschema import validate

try:
    from utils.i40data import Generic
except ImportError:
    from main.utils.i40data import Generic

try:
    from utils.utils import ExecuteDBModifier,ExecuteDBRetriever,AASMetaModelValidator,DescriptorValidator
except ImportError:
    from main.utils.utils import ExecuteDBModifier,ExecuteDBRetriever,AASMetaModelValidator,DescriptorValidator


class RetrieveMessage(Resource):    
    def __init__(self, pyAAS):
        self.pyAAS = pyAAS
        
    def post(self,aasId):
        jsonMessage = request.json
        try:
            if (jsonMessage["frame"]["sender"]["identification"]["id"] == self.pyAAS.AASID):
                pass
            else:
                self.pyAAS.msgHandler.putIbMessage(jsonMessage)
        except:
            pass

class AAS(Resource):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
    
    def get(self,aasId):
        try:
            edbR = ExecuteDBRetriever(self.pyAAS)
            dataBaseResponse = edbR.execute({"data":{"updateData":"emptyData","aasId":aasId},"method":"getAAS"})            
            return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
        except:
            return make_response("Unexpected Internal Server Error",500)
        
    def put(self,aasId):
        aasValid = AASMetaModelValidator(self.pyAAS)
        try:
            data = request.json
            if "interactionElements" in data:
                pass
                #return self.pyAAS.skillInstanceDict["AASHandler"].restAPIHandler(data)
            else:            
                if(aasValid.valitdateAAS(data)):
                    if (aasId == data["assetAdministrationShells"][0]["idShort"]):
                        edm = ExecuteDBModifier(self.pyAAS)
                        dataBaseResponse = edm.executeModifer({"data":{"updateData":data,"aasId":aasId},"method":"putAAS"})
                        return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
                    else:
                        return make_response("The namspace AASID value and the IdShort value do not match",500)
                else :
                    return make_response("The syntax of the passed Asset Administration Shell is not valid or malformed request",400)
        except Exception as E:
            return make_response("Internal Server Error",500)
    
    def delete(self,aasId):
        try:
            edm = ExecuteDBModifier(self.pyAAS)
            dataBaseResponse = edm.executeModifer({"data":{"updateData":"empty","aasId":aasId},"method":"deleteAASByID"})            
            return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
        except Exception as E:
            return make_response("Unexpected Internal Server Error",500)

        
class AASSubModels(Resource):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
        
    def get(self,aasId):
        try:
            edbR = ExecuteDBRetriever(self.pyAAS)
            dataBaseResponse = edbR.execute({"data":{"updateData":"emptyData","aasId":aasId},"method":"getSubmodels"})            
            return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
        except:
            return make_response("Unexpected Internal Server Error",500)
        
    def put(self,aasId):
        aasValid = AASMetaModelValidator(self.pyAAS)
        try:
            data = request.json
            if "interactionElements" in data:
                pass
                #return self.pyAAS.skillInstanceDict["AASHandler"].restAPIHandler(data)
            else:
                if(aasValid.valitdateSubmodel(data)):
                    edm = ExecuteDBModifier(self.pyAAS)
                    dataBaseResponse = edm.executeModifer({"data":{"updateData":data,"aasId":aasId},"method":"putSubmodels"})                     
                    return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
                else:
                    return make_response("The syntax of the passed submodel data is not valid or malformed request",400) 
        except Exception as E:
            return make_response("Unexpected Internal Server Error",500)
    
class AASSubmodelbyId(Resource):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
        
    def get(self,aasId,submodelId):
        try:
            edbR = ExecuteDBRetriever(self.pyAAS)
            dataBaseResponse = edbR.execute({"data":{"updateData":"emptyData","aasId":aasId,"submodelId":submodelId},"method":"getSubmodelsbyId"})            
            return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
        except:
            return make_response("Unexpected Internal Server Error",500)
        
    def put(self,aasId,submodelId):
        aasValid = AASMetaModelValidator(self.pyAAS)
        try:
            data = request.json
            if "interactionElements" in data:
                pass
                #return self.pyAAS.skillInstanceDict["AASHandler"].restAPIHandler(data)
            else:
                if(aasValid.valitdateSubmodel({"submodels":[data]})):
                    if (data["idShort"] == submodelId):
                        edm = ExecuteDBModifier(self.pyAAS)
                        dataBaseResponse = edm.executeModifer({"data":{"updateData":{"submodels":[data]},"aasId":aasId,"submodelId":submodelId},"method":"putSubmodels"})            
                        return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
                    else:
                        return make_response("The namspace SubmodelId value and the IdShort value do not match",500)
                else:
                    return make_response("The syntax of the passed submodel data is not valid or malformed request",400)
        except Exception as E:
            return make_response("Unexpected Internal Server Error",500)

    def delete(self,aasId,submodelId):
        try:
            edm = ExecuteDBModifier(self.pyAAS)
            dataBaseResponse = edm.executeModifer({"data":{"updateData":"empty","aasId":aasId,"submodelId":submodelId},"method":"deleteSubmodelsbyId"})            
            return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
        except Exception as E:
            return make_response("Unexpected Internal Server Error",500)
    

class AASDesc(Resource):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
    
    def get(self):
        try:
            edbR = ExecuteDBRetriever(self.pyAAS)
            dataBaseResponse = edbR.execute({"data":{"updateData":"emptyData"},"method":"getAllDesc"})
            return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
        except Exception as e:
            return make_response("Unexpected Internal Server Error"+str(e),500)

class AASDescbyId(Resource):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
    
    def get(self,aasId):
        try:
            edbR = ExecuteDBRetriever(self.pyAAS)
            dataBaseResponse = edbR.execute({"data":{"updateData":"emptyData","aasId":aasId},"method":"getAASDescByID"})            
            return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
        except Exception as e:
            return make_response("Unexpected Internal Server Error",500)
                
    def put(self,aasId):
        descValid = DescriptorValidator(self.pyAAS)
        try:
            data = request.json
            if "interactionElements" in data:
                return self.pyAAS.skillInstanceDict["RegistryHandler"].restAPIHandler(data)
            else:
                if(descValid.valitdateAASDescriptor(data)):
                    if (aasId == data["idShort"]):
                        edm = ExecuteDBModifier(self.pyAAS)
                        dataBaseResponse = edm.executeModifer({"data":{"updateData":data,"aasId":aasId},"method":"putAASDescByID"})              
                        return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
                    else:
                        return make_response("The namspace AASID value and the IdShort value do not match",500)
                else :
                    return make_response("The syntax of the passed Asset Administration Shell descriptor is not valid or malformed request",400)
        except Exception as E:
            return make_response("Unexpected Internal Server Error",500)
        
    def delete(self,aasId):
        try:
            edm = ExecuteDBModifier(self.pyAAS)
            dataBaseResponse = edm.executeModifer({"data":{"updateData":"emptyData","aasId":aasId},"method":"deleteAASDescById"})              
            return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
        except Exception as E:
            return make_response("Unexpected Internal Server Error",500)
        
class AASSubModelDescAASId(Resource):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
        
    def get(self,aasId):
        try:
            edbR = ExecuteDBRetriever(self.pyAAS)
            dataBaseResponse = edbR.execute({"data":{"updateData":"emptyData","aasId":aasId},"method":"getSubmodelDescByAASId"})            
            return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
        except Exception as E:
            return make_response("Unexpected Internal Server Error",500)
        
class AASSubModelDescbyId(Resource):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
    
    def get(self,aasId,submodelId):
        try:
            edbR = ExecuteDBRetriever(self.pyAAS)
            dataBaseResponse = edbR.execute({"data":{"updateData":"emptyData","aasId":aasId,"submodelId":submodelId},"method":"getSubmodelDescByID"})            
            return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
        except:
            return make_response("Unexpected Internal Server Error",500)
                
    def put(self,aasId,submodelId):
        descValid = DescriptorValidator(self.pyAAS)
        try:
            data = request.json
            if "interactionElements" in data:
                pass
                #return self.pyAAS.skillInstanceDict["RegistryHandler"].restAPIHandler(data)
            else:
                message = {"submodelDescriptors":[data]}
                if(descValid.valitdateSubmodelDescriptor(message)):
                    if (submodelId == data["idShort"]):
                        edm = ExecuteDBModifier(self.pyAAS)
                        dataBaseResponse = edm.executeModifer({"data":{"updateData":data,"aasId":aasId,"submodelId":submodelId},"method":"putSubmodelDescByID"})            
                        return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
                    else:
                        return make_response("The Namespace SubmodelId value and the IdShort value in the data are not matching",500)  
                else :
                    return make_response("The syntax of the passed Asset Administration Shell is not valid or malformed request",400)
        except Exception as E:
            return make_response("Unexpected Internal Server Error",500)

    def delete(self,aasId,submodelId):
        try:
            edm = ExecuteDBModifier(self.pyAAS)
            dataBaseResponse = edm.executeModifer({"data":{"updateData":"emptyData","aasId":aasId,"submodelId":submodelId},"method":"deleteSubmodelDescByID"})              
            return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
        except Exception as E:
            return make_response("Unexpected Internal Server Error",500)
             

