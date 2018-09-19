import sqlite3
print("In DatabaseContainer.py")

class DatabaseContainer(object):

	def __init__(self, pathToDatabase):
	
		# Connect to database immediately
		self.connection = None
		
		try:
			self.connection = sqlite3.connect(pathToDatabase)
			print ("Made connection!")
		except Error as e:
			print(e)
	 