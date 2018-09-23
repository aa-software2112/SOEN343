from application.Controllers.Controller import Controller

class UserController(Controller):
	
	def __init__(self, database):
		Controller.__init__(self, database)

	def exampleUserControllerFunction(self):
		print("User Controller")

	def loginHandler(self):
		get_clients_login_info = ''' SELECT username, password, isAdmin from client '''

		get_clients_cursor = self.db.executeQuery(get_clients_login_info, inputParameters=None)

		clients_login_info = get_clients_cursor.fetchall()

		for clients in clients_login_info:
			print(clients)

		return clients_login_info