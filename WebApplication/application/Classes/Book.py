class Book:
	def __init__(self, attributes):
		self._id = attributes['id']
		self._author = attributes['author']
		self._title = attributes['title']
		self._format = attributes['format']
		self._pages = attributes['pages']
		self._publisher = attributes['publisher']
		self._year_of_publication = attributes['year_of_publication']
		self._language = attributes['language']
		self._ISBN10 = attributes['isbn_10']
		self._ISBN13 = attributes['isbn_13']

	def get_id(self):
		"""Returns the id of the object"""
		return self._id
		
	def __str__(self):

		return "Book | ID: " + str(self._id) + " TITLE: " + self._title + " AUTHOR: " + self._author + " FORMAT: " + self._format + " PAGES: " + str(self._pages) + " PUBLISHER: " + self._publisher + " YEAR: " + self._year_of_publication + \
				" LANGUAGE: "  + self._language + " ISBN10: " + self._ISBN10 + " ISBN13: " + self._ISBN13
