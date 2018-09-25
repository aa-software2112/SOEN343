from application.Controllers.Controller import Controller

class UserController(Controller):
	
	def __init__(self, database):
		Controller.__init__(self, database)

	def exampleUserControllerFunction(self):
		print("User Controller")

	#function takes self and a string "username" to get the user from the client table.
	#returns none with message or displays client information and returns client row.
	def getClientByUsername(self, username):
		#to delete: sqlGetClientByUsername = ''' Select * From client Where username = ? , ('''username''',)'''
		getClientCursor = self.db.executeQuery("Select * From client Where username = ?", (username,))
		foundClient = getClientCursor.fetchone()

		if foundClient == None:
			print("There are no client with given Username")
		else:
			print(foundClient)
		
		return foundClient

	#function takes self and a string "email" to get the user from the client table.
	#returns none with message or displays client information and returns client row.
	def getClientByEmail(self, email):
		getClientCursor = self.db.executeQuery("Select * From client Where username = ?", (email,))
		foundClient = getClientCursor.fetchone()
		
		if foundClient == None:
			print("There are no client with given Username")
		else:
			print(foundClient)
		
		return foundClient

	#function takes self and a string "email" to get the user from the client table.
	#returns none with message or displays client information and returns client row.
	def getClientByPassword(self, username, password):
		get_client_cursor = self.db.executeQuery("Select * From client Where username = ? AND password = ?", (username, password))
		found_client = get_client_cursor.fetchone()
		found_client_list = []
		found_client_list.append(found_client)
		if found_client == None:
			print("There are no client with given Username and password")
		else:
			print(found_client_list)
		
		return found_client_list

	#function takes self and a values to create
	#creates a new client into the client table
	def createClient(self,firstName,lastName,physicalAddress,email,phoneNumber,username,password,isAdmin,isLogged,lastLogged):
		getClientByUsername = self.getClientByUsername(username)
		getClientByEmail = self.getClientByEmail(username)
		
		if getClientByUsername == None & getClientByEmail == None:
			sqlInsertClient = ''' INSERT INTO client(firstName,lastName,physicalAddress,email,phoneNumber,username,password,isAdmin,isLogged,lastLogged)
					VALUES(?,?,?,?,?,?,?,?,?,?) '''
		
			client = (firstName,lastName,physicalAddress,email,phoneNumber,username,password,isAdmin,isLogged,lastLogged)
			self.db.executeQuery(sqlInsertClient, client)
		else:
			getClientByUsername


