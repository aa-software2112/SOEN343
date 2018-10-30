from app.controllers.user_controller import UserController
from app.classes.client_container import Client
from app.classes.album import Album
from app.classes.book import Book
from app.classes.magazine import Magazine
from app.classes.movie import Movie
import app.common_definitions.helper_functions as helper_functions


class AdminController(UserController):

    def __init__(self, database, catalog_controller):
        UserController.__init__(self, database)
        # Admin Controller should have an instance of catalog controller
        self._catalog_controller = catalog_controller

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

    # Function to get a list of all logged clients to send to
    # UserResgitryViewer
    def get_all_logged_client(self):

        # instantiating the returning list
        allLoggedClientList = []
        getAllLoggedClientQuery = '''SELECT * FROM client WHERE isLogged=1 '''
        getClientCursor = self.db.execute_query(getAllLoggedClientQuery)
        loggedClients = getClientCursor.fetchall()

        # loggedClients contains a list with the attributes that the cursor reads from a row in ONE SINGLE string, so something like loggedClients[0].id does not work
        # instead loggedClients[0] returns a DICTIONARY of all the attributes
        # it found on the first ROW in the table
        for row in loggedClients:
            # Appending a Client object from the rows obtained by the SQL query
            client = Client(row)
            # convert to a readable timestamp
            client.lastLogged = helper_functions.convert_epoch_to_datetime(
                client.lastLogged)
            print(client)
            allLoggedClientList.append(client)

        print()
        return allLoggedClientList

    # Creates admin using create_client method in UserController.
    def create_admin(self, firstName, lastName, physicalAddress, email, phoneNumber, username, password, isAdmin,
                     isLogged, lastLogged):
        if isAdmin == 1:
            UserController.create_client(self, firstName, lastName, physicalAddress, email, phoneNumber, username,
                                         password, isAdmin, isLogged, lastLogged)
        else:
            print("When creating admin, make sure you call this function with a value of 1 for the attribute isAdmin.")

    def view_inventory(self):
        return self._catalog_controller.get_all_catalogs()

    def get_book_by_id(self, id):
        return self._catalog_controller.get_book_by_id(id)

    def get_magazine_by_id(self, id):
        return self._catalog_controller.get_magazine_by_id(id)

    def get_album_by_id(self, id):
        return self._catalog_controller.get_album_by_id(id)

    def get_movie_by_id(self, id):
        return self._catalog_controller.get_movie_by_id(id)

    def add_new_catalog(self, type, request_form):
        if (type == 1):
            return self._catalog_controller.add_book_to_catalog(Book(request_form))

        elif (type == 2):
            return self._catalog_controller.add_movie_to_catalog(Movie(request_form))

        elif (type == 3):
            return self._catalog_controller.add_magazine_to_catalog(Magazine(request_form))

        elif (type == 4):
            return self._catalog_controller.add_album_to_catalog(Album(request_form))

    def modify_catalog(self, type, request_form):
        if (type == 1):
            self._catalog_controller.view_catalog_inventory(
            )[self._catalog_controller.BOOK_TYPE].modify(Book(request_form))

        elif (type == 2):
            self._catalog_controller.view_catalog_inventory(
            )[self._catalog_controller.MOVIE_TYPE].modify(Movie(request_form))

        elif (type == 3):
            self._catalog_controller.view_catalog_inventory(
            )[self._catalog_controller.MAGAZINE_TYPE].modify(Magazine(request_form))

        elif (type == 4):
            self._catalog_controller.view_catalog_inventory(
            )[self._catalog_controller.ALBUM_TYPE].modify(Album(request_form))

    def delete_catalog(self, id, type):
        self._catalog_controller.view_catalog_inventory()[type].remove(id)
