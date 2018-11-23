from app.controllers.controller import Controller
import app.classes.catalogs
from app.classes.user import Admin, Client
from app.classes.database_container import DatabaseContainer
import app.controllers.catalog_controller
import time

class ClientController(Controller):
    """
    This class uses the Singleton pattern.
    """
    _instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if ClientController._instance is None:
            ClientController._instance = ClientController()
        return ClientController._instance

    def __init__(self):
        if ClientController._instance is not None:
            raise Exception("This class is a singleton!")

        else:
            ClientController._instance = self
            Controller.__init__(self, DatabaseContainer.get_instance())

            self._db_loaded = False
            self._client_catalog = app.classes.catalogs.UserCatalog()
            self._catalog_controller = app.controllers.catalog_controller.CatalogController.get_instance()
            self._loan_catalog = app.classes.catalogs.LoanCatalog.get_instance()

    def load_database_into_memory(self):

        # Database cannot be loaded into RAM more than once.
        if not self._db_loaded:
            self._db_loaded = True

        # Add all objects form database into catalogs
        sql_query = """ SELECT * FROM client WHERE isAdmin = 0 """

        all_rows = self.db.execute_query(sql_query).fetchall()

        # Create an object for each row
        for row in all_rows:
            self._client_catalog.add(Client(row), False)

        # Uncomment these two lines to see all objects in all catalogs
        #for k, v in self._client_catalog.get_all().items():
        #    print(v)

    def get_all_logged_clients(self):
        all_clients = list(self._client_catalog.get_all().values())
        logged_clients = [client for client in all_clients if client._is_logged == 1]
        return logged_clients


    # function takes self and a string "username" to get the user from the client table.
    # returns list with client information or emptylist if client doesn't
    # exist in database
    def get_client_by_username(self, username):

        found_client = []

        clients = self._client_catalog.get_all()

        for id, clientObj in clients.items():

            if clientObj._username == username:
                found_client.append(clientObj)

        return found_client

    # function takes self and a string "email" to get the user from the client table.
    # returns list with client information or emptylist if client doesn't
    # exist in database
    def get_client_by_email(self, email):


        found_client = []

        clients = self._client_catalog.get_all()

        for id, clientObj in clients.items():

            if clientObj._email == email:
                found_client.append(clientObj)

        return found_client

    # function takes self and a string "username" & "password" to get the client from the client table.
    # if client exits, returns list with client information and updates value
    # in attribute isLogged to 1. Returns emptylist if client doesn't exist in
    # database
    def get_client_by_password(self, username, password):

        found_client = []

        clients = self._client_catalog.get_all()

        for id, clientObj in clients.items():

            if clientObj._username == username and clientObj._password == password:
                found_client.append(clientObj)

        return found_client

    def view_inventory(self):
        return self._catalog_controller.get_all_catalogs()

    def login_client(self, username):
        client = self.get_client_by_username(username)

        if len(client) == 1:
            client = client[0]
            client._is_logged = 1
            client._last_logged = time.time()
            self._client_catalog.modify(client)

    # function takes self and username
    # updates value in attribute isLogged to 0.
    def logout_client(self, username):
        """
        self.db.execute_query_write(
            "UPDATE client SET isLogged = 0 WHERE username = ?", (username,))
        """

        client = self.get_client_by_username(username)

        # Mark client as logged out
        if len(client) == 1:
            client = client[0]
            client._is_logged = 0
            self._client_catalog.modify(client)

        print("Client has been logged out")

        return True

    # function takes self and several values to create a client
    # inserts a new client into the client table
    def create_client(self, firstName, lastName, physicalAddress, email, phoneNumber, username, password,
                      isLogged, lastLogged):

        attributesDict = {"firstName": firstName, "lastName": lastName, "physicalAddress": physicalAddress,
                          "email": email, "phoneNumber": phoneNumber, "username": username, "password": password,
                          "isAdmin": 0, "isLogged": isLogged, "lastLogged": lastLogged}

        self._client_catalog.add(Client(attributesDict), True)

    def sort_by(self, catalog_type, sort_key_values, client_id):
        usr = self._client_catalog.get(client_id)
        last_searched_list = usr.get_last_searched_list()
        lst = self._catalog_controller.sort_by(catalog_type, sort_key_values, last_searched_list)
        usr.set_last_searched_list(lst)
        return lst

    def get_next_item(self, client_id):

        client_performing_search = self._client_catalog.get(client_id)

        return client_performing_search.get_next_record_searched()

    def get_last_searched_list(self, client_id):

        client_performing_search = self._client_catalog.get(client_id)

        return client_performing_search.get_last_searched_list()


    def add_list_to(self, client_id, list_to_add):

        usr = self._client_catalog.get(client_id)

        usr.set_last_searched_list(list_to_add)

        return

    def filter_by(self, catalog_type, filter_key_values, client_id):
      
        usr = self._client_catalog.get(client_id)
        last_searched_list = usr.get_last_searched_list()
        lst = self._catalog_controller.filter_by(catalog_type, filter_key_values, last_searched_list)
        usr.set_last_searched_list(lst)
        return lst
      
    def search_from(self, catalog_type, search_value, client_id):

        usr = self._client_catalog.get(client_id)

        if search_value.strip() == "":
            return usr.get_last_searched_list()

        lst = self._catalog_controller.search_from(catalog_type, search_value)
        usr.set_last_searched_list(lst)

        return lst

    def set_detailed_view_index(self, record_object, client_id):
        usr = self._client_catalog.get(client_id)
        index = usr.get_index_from_object(record_object)
        usr.set_index_last_searched(index)

    # returns the cart set from the specific client with 'client_id'
    def get_all_cart_items(self, client_id):
      
        # Extract the user
        client = self._client_catalog.get(client_id)

        # Extract the cart
        cart_set = client.get_cart_set()

        return cart_set

    # deletes the item specified by 'o_id' from cart and returns the updated cart
    def delete_from_cart(self, o_id, user_id):
        usr = self._client_catalog.get(user_id)
        # returns the message passed success/error
        return usr.delete_from_cart(o_id)

    def get_loaned_items(self, client_id):
        usr = self._client_catalog.get(client_id)

        '''Test'''
        loan1 = {'_id': 1, '_name': 'My first loan'}
        loan2 = {'_id': 2, '_name': 'My second loan'}
        loan3 = {'_id': 3, '_name': 'My third loan'}
        user_loans = [loan1, loan2, loan3]
        usr.set_loan_list(user_loans)
        ''''''

        loaned_items = usr.get_loaned_items()

        return loaned_items

    def return_loaned_items(self, loaned_items_ids, client_id):
        usr = self._client_catalog.get(client_id)
        for loan_id in loaned_items_ids:
            self._loan_catalog.return_loaned_items(loan_id)
            usr.remove_loan(loan_id)
