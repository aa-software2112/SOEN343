class Magazine:
	def __init__(self,arguments):
		#Currently from CatalogController, the .fetchall() returns a sqlite3.row object, so I convert it to a dictionary to search the 'id' key
		if 'id' in dict(arguments):
			self._id = arguments['id']
		else:
			self._id = 0
		self._title = arguments['title']
		self._publisher = arguments['publisher']
		self._year_of_publication = arguments['year_of_publication']
		self._language = arguments['language']
		self._ISBN10 = arguments['isbn_10']
		self._ISBN13 = arguments['isbn_13']

	def get_id(self):
		"""Returns the id of the object"""
		return self._id

	def __str__(self):

		return "Magazine | ID: " + str(self._id) + " TITLE: " + self._title +  " PUBLISHER: " + self._publisher + " YEAR: " + self._year_of_publication + \
				" LANGUAGE: "  + self._language + " ISBN10: " + self._ISBN10 + " ISBN13: " + self._ISBN13
