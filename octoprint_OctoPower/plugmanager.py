from octoprint_OctoPower.wemo import WemoAdapter
from octoprint_OctoPower.plugadapter import PlugAdapter

class PlugManager:
    __REGISTERED_ADAPTERS = [
        WemoAdapter()
    ]

    __devices = []

    def discoverPlugs(self):
        self.__devices = []
        for x in self.__REGISTERED_ADAPTERS:
            self.__devices += x.discover()

        return self.__devices

    def getCahcedPlugs(self):
        return self.__devices

    def findCachedPlug(self, uuid):
        for d in self.__devices:
            if d.getUUID() == uuid:
                return d

        return None

