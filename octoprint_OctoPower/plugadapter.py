from abc import ABCMeta, abstractmethod

class PlugAdapter():
    __metaclass__ = ABCMeta

    @abstractmethod
    def discover(self):
        raise NotImplementedError
    
