from application.Controllers.UserController import UserController

class AdminController(UserController):
	
	def __init__(self, database):
		UserController.__init__(self, database)

	def exampleAdminControllerFunction(self):
		print("Admin Controller")
	