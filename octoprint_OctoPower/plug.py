from abc import ABCMeta, abstractmethod

class Plug():
    __metaclass__ = ABCMeta

    @abstractmethod
    def getName(self):
        raise NotImplementedError

    @abstractmethod
    def getUUID(self):
        raise NotImplementedError

    @abstractmethod
    def on(self):
        raise NotImplementedError

    @abstractmethod
    def off(self):
        raise NotImplementedError


