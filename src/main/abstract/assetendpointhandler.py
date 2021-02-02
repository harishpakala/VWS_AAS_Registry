'''
Created on 17.09.2019

@author: pakala
'''

import abc



class AsssetEndPointHandler(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, saas, ip, port, username, password, propertylist):
        self.saas = saas
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password 
        self.propertylist = propertylist
        
    def add_raw_channel_ref(self, ref_id, address):
        self.raw_channel_refs[ref_id] = address

    def configure(self, ioAdaptor):
        """Configures the raw channels of the IOAdapter."""
        for channelRef in ioAdaptor["propertyReferences"]:
            channel = self.saas.channels[channelRef["propertyName"]]
            channel.io_adapter = channelRef["propertyName"]
            channel.io_address = channelRef["Address"]

    def read_channel(self, channel_id):
        """Returns a raw channel value."""
        channel = self.saas.channels[channel_id]
        value = self.read(channel.io_address)
        # print(value, "ww",channel.io_address)
        # if channel_id == "c4ad116c-e953-4aa7-a9e1-5785e786bc13":
            # print (value ,channel_id ,"dd")
        if channel.type == "str":
            return str(value)
        if channel.type == "int":
            return int(value)
        if channel.type == "float":
            return float(value)

    def write_channel(self, channel_id, value):
        """Writes a value to a raw channel."""
        channel = self.saas.channels[channel_id]
        if channel.type == "str":
            self.write(channel.address, str(value))
        if channel.type == "int":
            self.write(channel.address, int(value))
        if channel.type == "float":
            self.write(channel.address, float(value))

    @abc.abstractmethod
    def read(self, address):
        """Returns a value according to the given address. This operation
        should use sophisticated caching strategies to achieve fast
        access to the requested values, e.g. query full blocks of data
        and only if a certain time is gone since last real query of
        data from the asset.

        """
        pass

    @abc.abstractmethod
    def write(self, address, value):
        """Writes a value to the given address. This operation should use
        sophisticated caching strategies to achieve fast access to the
        requested values, e.g. transmit full blocks of data and only
        if a certain time is gone since last real query of data from
        the asset.

        """
        pass
