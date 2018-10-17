import abc
from application.Controllers.Controller import Controller

class Catalog(abc.ABC):
    """Abstract class Catalog"""

    @abc.abstractmethod
    def get_all(self):
        """This method returns a collection"""
        pass

    @abc.abstractmethod
    def get(self, id):
        """This method returns a single object from a collection"""
        pass

    @abc.abstractmethod
    def add(self, object):
        """This method adds a single object to a collection"""
        pass

    @abc.abstractmethod
    def modify(self, modifiedObject):
        """This method adds a single object to a collection"""
        pass

    @abc.abstractmethod
    def remove(self, id):
        """This method removes an object from the collection, the object is returned"""
        pass


class BookCatalog(Catalog):

	def __init__(self, database):
		Controller.__init__(self, database)
		# private variable convention in python have '_' prefix
		self._books = {}

	def get_all(self):
		return self._books

	def get(self, id):
		return self._books[id]

	def modify(self, modified_book):
		self._books[modified_book.get_id()] = modified_book

	def add(self, book, add_to_db):
		# can act as a modify too!
		book._id = len(self._books)+1
		self._books[book._id] = book
		if add_to_db is True:
			insert_new_book = 'INSERT INTO book(author,title,format,pages,publisher,year_of_publication,language,isbn_10,isbn_13)' \
					 'VALUES(?,?,?,?,?,?,?,?,?)'
			new_book = (book._author, book._title, book._format, book._pages, book._publisher, book._year_of_publication
						, book._language, book._ISBN10, book._ISBN13)
			self.db.executeQueryWrite(insert_new_book, new_book)

	def remove(self, id):
		return self._books.pop(id, None)

	def display(self):

		for k, v in self._books.items():
			print(v)


class MovieCatalog(Catalog):

	def __init__(self, database):

		self._movies = {}

	def get_all(self):
		return self._movies

	def get(self, id):
		return self._movies[id]

	def add(self, movie, add_to_db):
		movie._id = len(self._movies)+1
		self._movies[movie._id] = movie
		if add_to_db is True:
			insert_new_movie = 'INSERT INTO movie(title, director, producers, actors, language, subtitles, dubbed, release_date, run_time)' \
					 'VALUES(?,?,?,?,?,?,?,?,?)'
			new_movie = (movie._title, movie._director, movie._producers, movie._actors, movie._language, movie._subtitles, movie._dubbed
						 , movie._release_date, movie._runtime)
			self.db.executeQueryWrite(insert_new_movie, new_movie)

	def modify(self, movie):
		self._movies[movie.get_id()] = movie

	def remove(self, id):
		return self._movies.pop(id, None)

	def display(self):

		for k, v in self._movies.items():
			print(v)



class MagazineCatalog(Catalog):

	def __init__(self, database):
		Controller.__init__(self, database)
		self._magazines = {}

	def get_all(self):
		return self._magazines

	def get(self, id):
		return self._magazines[id]

	def add(self, magazine, add_to_db):
		magazine._id = len(self._magazines)+1
		self._magazines[magazine._id] = magazine
		if add_to_db is True:
			insert_new_magazine = 'INSERT INTO magazine(title, publisher, year_of_publication, language, isbn_10, isbn_13)' \
					 'VALUES(?,?,?,?,?,?)'
			new_magazine = (magazine._title, magazine._publisher, magazine._year_of_publication, magazine._language, magazine._ISBN10
							,magazine._ISBN13)
			self.db.executeQueryWrite(insert_new_magazine, new_magazine)

	def modify(self, magazine):
		self._magazines[magazine.get_id()] = magazine

	def remove(self, id):
		return self._magazines.pop(id, None)

	def display(self):

		for k, v in self._magazines.items():
			print(v)

class AlbumCatalog(Catalog):

	def __init__(self, database):
		Controller.__init__(self, database)
		self._albums = {}

	def get_all(self):
		return self._albums

	def get(self, id):
		return self._albums[id]

	def add(self, album, add_to_db):
		album._id = len(self._albums) + 1
		self._albums[album._id] = album
		if add_to_db is True:
			insert_new_album = 'INSERT INTO album(type, title, artist, label, release_date, asin) VALUES(?,?,?,?,?,?)'
			new_album = (album._type, album._title, album._artist, album._label, album._release_date, album._ASIN)
			self.db.executeQueryWrite(insert_new_album, new_album)

	def modify(self, album):
		self._albums[album.get_id()] = album

	def remove(self, id):
		return self._albums.pop(id, None)

	def display(self):
		
		for k, v in self._albums.items():
			print(v)


