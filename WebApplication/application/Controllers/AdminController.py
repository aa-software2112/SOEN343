from application.Controllers.UserController import UserController
from application.Classes.ClientContainer import Client
import application.CommonDefinitions.HelperFunctions as HelperFunctions

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

