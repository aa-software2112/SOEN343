from app.controllers.controller import Controller
from app.controllers.user_controller import ClientController
from app.classes.user import Admin
from app.classes.album import Album
from app.classes.book import Book
from app.classes.magazine import Magazine
from app.classes.movie import Movie
from app.classes.catalogs import UserCatalog
import app.common_definitions.helper_functions as helper_functions


class AdminController(Controller):

    def __init__(self, database, catalog_controller):
        Controller.__init__(self, database)

        # Admin Controller should have an instance of catalog controller
        self._catalog_controller = catalog_controller

        # Admin Controller contains a catalog of admin users
        self._admin_catalog = UserCatalog(database)

        self._db_loaded = False

    def example_admin_controller_function(self):
        print("Admin Controller")

    def example_admin_sql_call(self):

        # Create your query
        yourQuery = ''' SELECT * from client WHERE isLogged=1'''

        """ There is a DatabaseContainer object (see Database/DatabaseContainer.py) stored in every Controller (see Controllers/Controller.py)
		through this class' constructor __init__(...). It is sent all the way up the object hierarchy until it reaches the Controller object
		
		This database object abstracts stores the sqlite connection (see __init__.py in /application/). We need this
		encapsulation to control read/write requests later.
		
		This next line executes the query; it has an optional input parameter for write-based SQL queries; this example is a read-based one
		
		The function .executeQuery(...) returns the cursor created out of the execution of your query --> again, see Database/DatabaseContainer.py
		"""
        yourCursor = self.db.execute_query(yourQuery, inputParameters=None)

        # See
        # https://docs.python.org/2/library/sqlite3.html#sqlite3.Cursor.execute
        # for cursor functions
        yourResults = yourCursor.fetchall()

        # At this point, iterate over results and store them in some object (User, Book, Music, etc...) before returning
        # print("Results from exampleAdminSQLCall: ")
        # for result in yourResults:
        #	print(result)

        # Here you would return a list of objects
        return


    def get_all_logged_admins(self):

        return list(self._admin_catalog.get_all().values())

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
        #for k, v in self._admin_catalog.get_all().items():
        #    print(v)

    def logout_admin(self, username):
        admin = self.get_admin_by_username(username)

        # Mark admin as logged out
        if len(admin) == 1:
            admin = admin[0]
            admin._is_logged = 0
            self._admin_catalog.modify(admin)

        print("Admin has been logged out.")

    # Creates admin using create_client method in UserController.
    def create_admin(self, firstName, lastName, physicalAddress, email, phoneNumber, username, password, isLogged, lastLogged):

        attributesDict = {"firstName": firstName, "lastName": lastName, "physicalAddress":physicalAddress,
                          "email": email, "phoneNumber": phoneNumber, "username": username, "password": password,
                          "isAdmin":1, "isLogged":isLogged, "lastLogged": lastLogged}

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

    def get_catalog_entry_by_id(self,catalog_type, id):
        return self._catalog_controller.get_catalog_entry_by_id(catalog_type, id)

    def get_catalog_copies_by_id(self, catalog_type, id):
        return self._catalog_controller.get_catalog_entry_copies_by_id(catalog_type, id)

    def add_entry_to_catalog(self, type, request_form):
    
        if (type == self._catalog_controller.BOOK_TYPE):
            return self._catalog_controller.add_entry_to_catalog(type, Book(request_form))

        elif (type == self._catalog_controller.MOVIE_TYPE):
            return self._catalog_controller.add_entry_to_catalog(type, Movie(request_form))

        elif (type == self._catalog_controller.MAGAZINE_TYPE):
            return self._catalog_controller.add_entry_to_catalog(type, Magazine(request_form))

        elif (type == self._catalog_controller.ALBUM_TYPE):
            return self._catalog_controller.add_entry_to_catalog(type, Album(request_form))

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
  
    def filter_by(self, catalog_type, filter_key_values, admin_id):
      
        usr = self._admin_catalog.get(admin_id)
        last_searched_list = usr.get_last_searched_list()

    def sort_by(self, catalog_type, sort_key_values, admin_id):
      
        usr = self._admin_catalog.get(admin_id)
        last_searched_list = usr.get_last_searched_list()
        lst = self._catalog_controller.sort_by(catalog_type, sort_key_values, last_searched_list)
        usr.set_last_searched_list(lst)
        return lst

    def search_from(self, catalog_type, search_value, admin_id):
      
        lst = self._catalog_controller.search_from(catalog_type, search_value)
        usr = self._admin_catalog.get(admin_id)
        usr.set_last_searched_list(lst)
        return lst
