from app.controllers.controller import Controller
from app.classes.user import Admin
from app.classes.album import Album
from app.classes.book import Book
from app.classes.magazine import Magazine
from app.classes.movie import Movie
from app.classes.catalogs import UserCatalog
from app.classes.database_container import DatabaseContainer
from app.controllers.catalog_controller import CatalogController
import time


class AdminController(Controller):
    """
    This class uses the Singleton pattern.
    """
    _instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if AdminController._instance is None:
            AdminController._instance = AdminController()
        return AdminController._instance

    def __init__(self):
        if AdminController._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            AdminController._instance = self
            Controller.__init__(self, DatabaseContainer.get_instance())

            # Admin Controller should have an instance of catalog controller
            self._catalog_controller = CatalogController.get_instance()

            # Admin Controller contains a catalog of admin users
            self._admin_catalog = UserCatalog()

            self._db_loaded = False

    def get_all_logged_admins(self):
        all_admins = list(self._admin_catalog.get_all().values())
        logged_admins = [admin for admin in all_admins if admin._is_logged == 1]
        return logged_admins


    def load_database_into_memory(self):

        # Database cannot be loaded into RAM more than once
        if not (self._db_loaded):
            self._db_loaded = True

        # Add all objects form database into catalogs
        sql_query = """ SELECT * FROM client WHERE isAdmin = 1 """

        all_rows = self.db.execute_query(sql_query).fetchall()

        # Create an object for each row
        for row in all_rows:
            self._admin_catalog.add(Admin(row), False)

        # Uncomment these two lines to see all objects in all catalogs
        # for k, v in self._admin_catalog.get_all().items():
        #    print(v)

    def login_admin(self, username):
        admin = self.get_admin_by_username(username)

        if len(admin) == 1:
            admin = admin[0]
            admin._is_logged = 1
            admin._last_logged = time.time()
            self._admin_catalog.modify(admin)

    def logout_admin(self, username):
        admin = self.get_admin_by_username(username)

        # Mark admin as logged out
        if len(admin) == 1:
            admin = admin[0]
            admin._is_logged = 0
            self._admin_catalog.modify(admin)

        print("Admin has been logged out.")

    # Creates admin using create_client method in UserController.
    def create_admin(self, firstName, lastName, physicalAddress, email, phoneNumber, username, password, isLogged,
                     lastLogged):

        attributesDict = {"firstName": firstName, "lastName": lastName, "physicalAddress": physicalAddress,
                          "email": email, "phoneNumber": phoneNumber, "username": username, "password": password,
                          "isAdmin": 1, "isLogged": isLogged, "lastLogged": lastLogged}

        self._admin_catalog.add(Admin(attributesDict), True)

    def get_admin_by_username(self, username):

        found_admin = []

        admins = self._admin_catalog.get_all()

        for id, adminObj in admins.items():

            if adminObj._username == username:
                found_admin.append(adminObj)

        return found_admin

        # function takes self and a string "email" to get the user from the client table.
        # returns list with client information or emptylist if client doesn't
        # exist in database

    def get_admin_by_email(self, email):
        found_admin = []

        admins = self._admin_catalog.get_all()

        for id, adminObj in admins.items():

            if adminObj._email == email:
                found_admin.append(adminObj)

        return found_admin

        # function takes self and a string "username" & "password" to get the client from the client table.
        # if client exits, returns list with client information and updates value
        # in attribute isLogged to 1. Returns emptylist if client doesn't exist in
        # database

    def get_admin_by_password(self, username, password):

        found_admin = []

        admins = self._admin_catalog.get_all()

        for id, adminObj in admins.items():

            if adminObj._username == username and adminObj._password == password:
                found_admin.append(adminObj)

        return found_admin

    def view_inventory(self):
        return self._catalog_controller.get_all_catalogs()

    def get_catalog_entry_by_id(self, catalog_type, id):
        return self._catalog_controller.get_catalog_entry_by_id(catalog_type, id)

    def get_catalog_copies_by_id(self, catalog_type, id):
        return self._catalog_controller.get_catalog_entry_copies_by_id(catalog_type, id)

    def add_entry_to_catalog(self, catalog_type, request_form):

        return self._catalog_controller.add_entry_to_catalog(catalog_type, request_form)

    def modify_catalog(self, type, request_form):

        if (type == self._catalog_controller.BOOK_TYPE):
            self._catalog_controller.modify_catalog_entry(type, Book(request_form))

        elif (type == self._catalog_controller.MOVIE_TYPE):
            self._catalog_controller.modify_catalog_entry(type, Movie(request_form))

        elif (type == self._catalog_controller.MAGAZINE_TYPE):
            self._catalog_controller.modify_catalog_entry(type, Magazine(request_form))

        elif (type == self._catalog_controller.ALBUM_TYPE):
            self._catalog_controller.modify_catalog_entry(type, Album(request_form))

    def delete_catalog(self, id, type):
        self._catalog_controller.view_catalog_inventory()[type].remove(id)

    def delete_catalog_copy_entry(self, catalog_type, id):
        return self._catalog_controller.delete_catalog_entry_copy(catalog_type, id)

    def get_next_item(self, admin_id):

        admin_performing_search = self._admin_catalog.get(admin_id)

        return admin_performing_search.get_next_record_searched()

    def get_last_searched_list(self, admin_id):

        admin_performing_search = self._admin_catalog.get(admin_id)

        return admin_performing_search.get_last_searched_list()

    def add_list_to(self, admin_id, list_to_add):

        usr = self._admin_catalog.get(admin_id)

        usr.set_last_searched_list(list_to_add)

        return

    def filter_by(self, catalog_type, filter_key_values, admin_id):

        usr = self._admin_catalog.get(admin_id)
        last_searched_list = usr.get_last_searched_list()
        lst = self._catalog_controller.filter_by(catalog_type, filter_key_values, last_searched_list)
        usr.set_last_searched_list(lst)
        return lst

    def sort_by(self, catalog_type, sort_key_values, admin_id):

        usr = self._admin_catalog.get(admin_id)
        last_searched_list = usr.get_last_searched_list()
        lst = self._catalog_controller.sort_by(catalog_type, sort_key_values, last_searched_list)
        usr.set_last_searched_list(lst)
        return lst

    def search_from(self, catalog_type, search_value, admin_id):

        usr = self._admin_catalog.get(admin_id)

        if search_value.strip() == "":
            return usr.get_last_searched_list()

        lst = self._catalog_controller.search_from(catalog_type, search_value)
        usr.set_last_searched_list(lst)

        return lst

    def set_detailed_view_index(self, record_object, admin_id):
        usr = self._admin_catalog.get(admin_id)
        index = usr.get_index_from_object(record_object)
        usr.set_index_last_searched(index)

    def search_transaction_by(self, search_transaction_key_values):
        
        lst = self._catalog_controller.search_transaction_by(self, catalog_type,search_transaction_key_values)
        return lst

    def view_transaction_history(self):

        lst = self._catalog_controller.view_transaction_history()
        return lst
