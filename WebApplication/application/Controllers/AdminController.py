from application.Controllers.UserController import UserController
from application.Classes.ClientContainer import Client
import application.CommonDefinitions.HelperFunctions as HelperFunctions
from application.Classes.Album import Album
from application.Classes.Book import Book
from application.Classes.Magazine import Magazine
from application.Classes.Movie import Movie

class AdminController(UserController):
	
	def __init__(self, database, catalog_controller):
		UserController.__init__(self, database)
		# Admin Controller should have an instance of catalog controller 
		self._catalog_controller = catalog_controller

	def exampleAdminControllerFunction(self):
		print("Admin Controller")
		
	def exampleAdminSQLCall(self):
		
		# Create your query
		yourQuery = ''' SELECT * from client WHERE isLogged=1'''
	
		""" There is a DatabaseContainer object (see Database/DatabaseContainer.py) stored in every Controller (see Controllers/Controller.py)
		through this class' constructor __init__(...). It is sent all the way up the object hierarchy until it reaches the Controller object
		
		This database object abstracts stores the sqlite connection (see __init__.py in /application/). We need this
		encapsulation to control read/write requests later.
		
		This next line executes the query; it has an optional input parameter for write-based SQL queries; this example is a read-based one
		
		The function .executeQuery(...) returns the cursor created out of the execution of your query --> again, see Database/DatabaseContainer.py
		"""
		yourCursor = self.db.executeQuery(yourQuery, inputParameters=None)
		
		# See https://docs.python.org/2/library/sqlite3.html#sqlite3.Cursor.execute for cursor functions
		yourResults = yourCursor.fetchall()
			
		# At this point, iterate over results and store them in some object (User, Book, Music, etc...) before returning
		#print("Results from exampleAdminSQLCall: ")
		#for result in yourResults:
		#	print(result)
			
		# Here you would return a list of objects
		return
		
	#Function to get a list of all logged clients to send to UserResgitryViewer
	def getAllLoggedClient(self):

		#instantiating the returning list
		allLoggedClientList = []
		getAllLoggedClientQuery = '''SELECT * FROM client WHERE isLogged=1 '''
		getClientCursor = self.db.executeQuery(getAllLoggedClientQuery)
		loggedClients = getClientCursor.fetchall()

		#loggedClients contains a list with the attributes that the cursor reads from a row in ONE SINGLE string, so something like loggedClients[0].id does not work
		#instead loggedClients[0] returns a DICTIONARY of all the attributes it found on the first ROW in the table
		for row in loggedClients:
			#Appending a Client object from the rows obtained by the SQL query
			client = Client(row)
			# convert to a readable timestamp
			client.lastLogged = HelperFunctions.convertEpochToDatetime(client.lastLogged)
			print(client)
			allLoggedClientList.append(client)

		print()
		return allLoggedClientList

	#Creates admin using create_client method in UserController.
	def createAdmin(self,firstName,lastName,physicalAddress,email,phoneNumber,username,password,isAdmin,isLogged,lastLogged):
		if isAdmin == 1:
			UserController.createClient(self,firstName,lastName,physicalAddress,email,phoneNumber,username,password,isAdmin,isLogged,lastLogged)
		else:
			print("When creating admin, make sure you call this function with a value of 1 for the attribute isAdmin.")

	def view_inventory(self):
		return self._catalog_controller.get_all_catalogs()

	def add_new_book(self, request_form):
		return self._catalog_controller.add_book_to_catalog(Book(request_form))

	def add_new_magazine(self, request_form):
		return self._catalog_controller.add_magazine_to_catalog(Magazine(request_form))
	
	def add_new_album(self, request_form):
		return self._catalog_controller.add_album_to_catalog(Album(request_form))

	def add_new_movie(self, request_form):
		return self._catalog_controller.add_movie_to_catalog(Movie(request_form))

	#Modify takes a dictionary from the request form and passes an object created with the request form
	def modify_book(self, request_form):
		self._catalog_controller.view_catalog_inventory()[self._catalog_controller.BOOK_TYPE].modify(Book(request_form))

	def modify_magazine(self, request_form):
		self._catalog_controller.view_catalog_inventory()[self._catalog_controller.MAGAZINE_TYPE].modify(Magazine(request_form))

	def modify_album(self, request_form):
		self._catalog_controller.view_catalog_inventory()[self._catalog_controller.ALBUM_TYPE].modify(Album(request_form))

	def modify_movie(self, request_form):
		self._catalog_controller.view_catalog_inventory()[self._catalog_controller.MOVIE_TYPE].modify(Movie(request_form))

	def get_book_by_id(self,id):
		return self._catalog_controller.get_book_by_id(id)

	def get_magazine_by_id(self,id):
		return self._catalog_controller.get_magazine_by_id(id)

	def get_album_by_id(self,id):
		return self._catalog_controller.get_album_by_id(id)

	def get_movie_by_id(self,id):
		return self._catalog_controller.get_movie_by_id(id)

	def delete_catalog(self, id, type):
		self._catalog_controller.view_catalog_inventory()[type].remove(id)
