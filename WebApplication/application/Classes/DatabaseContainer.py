import sqlite3
import sys

print("In DatabaseContainer.py")

"""
Use dbVariableName.connection to create the cursor necessary for queries
"""
class DatabaseContainer(object):

	def __init__(self, pathToDatabase):
	
		# Connect to database immediately
		self.connection = None
		self.dbPath = pathToDatabase
		
		try:
			self.connection = sqlite3.connect(pathToDatabase)
			print ("Made connection!")
		except Error as e:
			print(e)
			sys.exit()
			
	"""
	This function executes a query and returns the cursor linked to the query
	The input parameter is optional
	"""
	def executeQuery(self, sqlQuery, inputParameters=None):
		
		# Create new cursor
		cursor = self.connection.cursor()
		
		if inputParameters == None:
			cursor.execute(sqlQuery)
		else:
			cursor.execute(sqlQuery, inputParameters)
			
		return cursor
	
	def closeConnection(self):
		try:
			self.connection.close()
		except Error as e:
			print(e)
	
	def printPath(self):
		print(self.dbPath)
	 