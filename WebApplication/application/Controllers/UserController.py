from application.Controllers.Controller import Controller
from application.Classes.ClientContainer import Client

class UserController(Controller):
	
	def __init__(self, database):
		Controller.__init__(self, database)

	def exampleUserControllerFunction(self):
		print("User Controller")

	# Temporary query handler
	def loginHandler(self, username):

		clients_data_list = []
		get_clients_data = ''' SELECT * from client WHERE username = ? '''

		get_clients_cursor = self.db.executeQuery(get_clients_data, [username])

		clients_data = get_clients_cursor.fetchall()

		for row in clients_data:
			clients_data_list.append(Client(row))

		for clients in clients_data:
			print(clients)
			print()

		return clients_data_list