from app.controllers.controller import Controller
import app.classes.catalogs
from app.classes.user import Admin, Client
from app.classes.database_container import DatabaseContainer
from app.classes.loan import Loan
from app.classes.book import Book
from app.classes.album import Album
from app.classes.movie import Movie
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

    def get_client_by_id(self, id):
        found_client = []

        clients = self._client_catalog.get_all()

        for id, clientObj in clients.items():

            if clientObj._id == id:
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

    def add_to_cart(self, catalog_type, object_id, user_id):

        print(catalog_type)

        o = self._catalog_controller.get_catalog_entry_by_id(catalog_type, object_id)
        print(o)
        old, new = self._client_catalog.add_to_cart(user_id, o)
        if old - new == 0:

            return "Item already exist in cart "
        else:

            return "Item added successfully"

    # deletes the item specified by 'o_id' from cart and returns the updated cart
    def delete_from_cart(self, o_id, user_id, record_type):
        usr = self._client_catalog.get(user_id)
        # returns the message passed success/error
        return usr.delete_from_cart(o_id, record_type)

    def load_loans_db_to_memory(self):
        # Database cannot be loaded into RAM more than once.
        if not self._db_loaded:
            self._db_loaded = True

        # Add all objects form database into catalogs
        sql_query = """ SELECT * FROM loan """

        all_rows = self.db.execute_query(sql_query).fetchall()

        # Create an object for each row
        for row in all_rows:
            # transforming the row from the query to a dictionary for easier method to access columns.
            row = dict(row)
            print(row['is_returned'])
            record_type = row['table_name']
            copy_id = row['record_id']
            # have to check the type of record in the loan table to then get a record obj, since Loan object requires an user obj and record obj as parameter
            if record_type == Book.copy_table_name:
                record_id = self._catalog_controller.get_record_id_by_copy_id(self._catalog_controller.BOOK_TYPE, row['record_id'])
                record_obj = self._catalog_controller.get_catalog_entry_by_id(self._catalog_controller.BOOK_TYPE,
                                                                              record_id)
                usr_obj = self._client_catalog.get(row['user_id'])
                loan = Loan(usr_obj, record_obj, copy_id)
                loan.set_loan_id(row['id'])
                loan.set_loan_time(row['loan_time'])
                loan.set_due_time(row['due_time'])
                loan.set_return_time(row['return_time'])
                loan.set_is_returned(row['is_returned'])
                if row['is_returned'] == 0:
                    usr_obj.add_to_loan_list(loan)
                self._loan_catalog.add(loan, False)
            if record_type == Album.copy_table_name:
                record_id = self._catalog_controller.get_record_id_by_copy_id(self._catalog_controller.ALBUM_TYPE,
                                                                              row['record_id'])
                record_obj = self._catalog_controller.get_catalog_entry_by_id(self._catalog_controller.ALBUM_TYPE,
                                                                              record_id)
                usr_obj = self._client_catalog.get(row['user_id'])
                loan = Loan(usr_obj, record_obj, copy_id)
                loan.set_loan_id(row['id'])
                loan.set_loan_time(row['loan_time'])
                loan.set_due_time(row['due_time'])
                loan.set_return_time(row['return_time'])
                loan.set_is_returned(row['is_returned'])
                if row['is_returned'] == 0:
                    usr_obj.add_to_loan_list(loan)
                self._loan_catalog.add(loan, False)
            if record_type == Movie.copy_table_name:
                record_id = self._catalog_controller.get_record_id_by_copy_id(self._catalog_controller.MOVIE_TYPE,
                                                                              row['record_id'])
                record_obj = self._catalog_controller.get_catalog_entry_by_id(self._catalog_controller.MOVIE_TYPE,
                                                                              record_id)
                usr_obj = self._client_catalog.get(row['user_id'])
                loan = Loan(usr_obj, record_obj, copy_id)
                loan.set_loan_id(row['id'])
                loan.set_loan_time(row['loan_time'])
                loan.set_due_time(row['due_time'])
                loan.set_return_time(row['return_time'])
                loan.set_is_returned(row['is_returned'])
                if row['is_returned'] == 0:
                    usr_obj.add_to_loan_list(loan)
                self._loan_catalog.add(loan, False)

        # Uncomment these two lines to see all objects in all catalogs
        # for k, v in self._client_catalog.get_all().items():
        #    print(v)

    def get_loaned_items(self, client_id):

        usr = self._client_catalog.get(client_id)
        loaned_items = usr.get_loaned_items()
        print(loaned_items)
        return loaned_items

    def return_loaned_items(self, loaned_items_ids, client_id):
        failed_loans = []
        for loan_id in loaned_items_ids:
            loan_id = self._loan_catalog.return_loaned_item(loan_id)
            if loan_id is not None:
                loan = self._loan_catalog.get(loan_id)
                failed_loans.append(loan)
        print(failed_loans == [])
        if failed_loans == []:
            usr = self._client_catalog.get(client_id)
            for loan_id in loaned_items_ids:
                usr.remove_loan(loan_id)
        return failed_loans

    def make_loan(self, client_id):
        usr = self._client_catalog.get(client_id)
        commits = usr.make_loan()

        return commits

