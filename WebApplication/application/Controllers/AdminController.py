from application.Controllers.UserController import UserController

class AdminController(UserController):
	
	def __init__(self, database):
		UserController.__init__(self, database)

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
		for result in yourResults:
			print (result)
			
		# Here you would return a list of objects
		return 
			