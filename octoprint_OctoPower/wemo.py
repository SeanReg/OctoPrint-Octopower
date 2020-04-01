from octoprint_OctoPower.plugadapter import PlugAdapter
from octoprint_OctoPower.plug import Plug

import pywemo

class WemoPlug(Plug):
    __wemoDevice = None

    def __init__(self, wemoDevice):
        self.__wemoDevice = wemoDevice

    def getName(self):
        return self.__wemoDevice.name

    def getUUID(self):
        return self.__wemoDevice.mac
    
    def on(self):
        self.__wemoDevice.on()

    def off(self):
        self.__wemoDevice.off()


class WemoAdapter(PlugAdapter):

    def discover(self):
        switches = filter(lambda x: isinstance(x, pywemo.Switch), pywemo.discover_devices())
        return [WemoPlug(x) for x in switches]