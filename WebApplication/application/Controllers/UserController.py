from application.Controllers.Controller import Controller
from application.Classes.ClientContainer import Client

class UserController(Controller):
	
	def __init__(self, database):
		Controller.__init__(self, database)

	def exampleUserControllerFunction(self):
		print("User Controller")

	#function takes self and a string "email" to get the user from the client table.
	#returns none with message or displays client information and returns client row.
	def getClientByPassword(self, username, password):
		get_client_cursor = self.db.executeQuery("Select * From client Where username = ? AND password = ?", (username, password))
		
		found_client = get_client_cursor.fetchmany(1)
		found_client_list = []

		for row in found_client:
			found_client_list.append(Client(row))
		
		if found_client == []:
			print("There are no client with given Username and password")
			return []
		else:
			print(found_client_list)
			return found_client_list

	# # Temporary query handler
	# def loginHandler(self, username, password):

	# 	clients_data_list = []
	# 	get_clients_data = ''' Select * From client Where username = ? AND password = ? '''

	# 	get_clients_cursor = self.db.executeQuery(get_clients_data, (username, password))

	# 	clients_data = get_clients_cursor.fetchall()

	# 	for row in clients_data:
	# 		clients_data_list.append(Client(row))

	# 	for clients in clients_data:
	# 		print(clients)
	# 		print()

	# 	return clients_data_list