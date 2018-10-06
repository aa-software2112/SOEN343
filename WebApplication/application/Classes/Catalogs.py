import abc

# Abstract class Catalog
class Catalog(abc.ABC):

    @abc.abstractmethod
    def getAll(self):
        pass
    @abc.abstractmethod
    def get(self, id):
        pass
    @abc.abstractmethod
    def add(self, resource):
        pass
    @abc.abstractmethod
    def remove(self, id):
        pass






