'''
Copyright (c) 2021-2022 OVGU LIA
Author: Harish Kumar Pakala
This source code is licensed under the Apache License 2.0 (see LICENSE.txt).
This source code may use other Open Source software components (see LICENSE.txt).
'''
from datetime import datetime
import uuid


class Channel(object):
    """The channel representation."""

    def __init__(self, pyAAS):
        self.pyAAS = pyAAS
        self.io_adapter = None  
        self.io_address = None
        self.current_value = None


    def configure(self, channel):
        self.id = channel["propertyName"]
        self.name = channel["propertyName"]
        self.type = "float"
      

    def set_io_adapter(self, io_adapter):
        self.io_adapter = io_adapter

    def read(self):
        if self.io_adapter is None:
            return self.current_value
            # TODO: think about to retrieve last value of the database channel
        else:
            adapter = self.saas.io_adapters[self.io_adapter]
            return adapter.read_channel(self.id)

    def write(self, value):
        self.current_value = value
        if self.io_adapter is None:
            # TODO: think about to put the value into the database channel
            pass
        else:
            self.io_adapter.write_channel(self.id, value)

    def update(self):
        
        newvalueDict = {}
        newvalueDict['name'] = self.name
        newvalueDict['channel_id'] = self.id
        newvalueDict['value'] = self.read()
        newvalueDict['datetimestamp'] = str(datetime.now())
        newvalueDict['id'] = uuid.uuid4()
        self.saas.msgHandler.putAssetMessage(newvalueDict)
