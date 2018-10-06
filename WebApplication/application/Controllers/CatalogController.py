from application.Controllers.Controller import Controller

class CatalogController(Controller):

    def __init__(self, database, catalog_list):
        Controller.__init__(self, database)
        self._inventory = catalog_list

    def viewInventory(self):
        return self._inventory



