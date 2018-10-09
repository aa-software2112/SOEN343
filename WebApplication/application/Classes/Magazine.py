class Magazine:
	def __init__(self,arguments):
		self._id = arguments['id']
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
