import abc
from application.Classes.Book import Book
from application.Classes.Movie import Movie
from application.Classes.Magazine import Magazine
from application.Classes.Album import Album

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

	def __init__(self):
		# private variable convention in python have '_' prefix
		self._books = {}

	def get_all(self):
		return self._books

	def get(self, id):
		return self._books[id]

	def modify(self, modified_book):
		self._books[modified_book.get_id()] = modified_book

	def add(self, book):
		# can act as a modify too!
		book._id = len(self._books)+1
		self._books[book._id] = book

	def remove(self, id):
		return self._books.pop(id, None)

	def display(self):

		for k, v in self._books.items():
			print(v)


class MovieCatalog(Catalog):

	def __init__(self):
		self._movies = {}

	def get_all(self):
		return self._movies

	def get(self, id):
		return self._movies[id]

	def add(self, movie):
		movie._id = len(self._movies)+1
		self._movies[movie._id] = movie

	def modify(self, movie):
		self._movies[movie.get_id()] = movie

	def remove(self, id):
		return self._movies.pop(id, None)

	def display(self):

		for k, v in self._movies.items():
			print(v)



class MagazineCatalog(Catalog):

	def __init__(self):
		self._magazines = {}

	def get_all(self):
		return self._magazines

	def get(self, id):
		return self._magazines[id]

	def add(self, magazine):
		magazine._id = len(self._magazines)+1
		self._magazines[magazine._id] = magazine

	def modify(self, magazine):
		self._magazines[magazine.get_id()] = magazine

	def remove(self, id):
		return self._magazines.pop(id, None)

	def display(self):

		for k, v in self._magazines.items():
			print(v)

class AlbumCatalog(Catalog):

	def __init__(self):
		self._albums = {}

	def get_all(self):
		return self._albums

	def get(self, id):
		return self._albums[id]

	def add(self, album):
		album._id = len(self._albums) + 1
		self._albums[album._id] = album

	def modify(self, album):
		self._albums[album.get_id()] = album

	def remove(self, id):
		return self._albums.pop(id, None)

	def display(self):
		
		for k, v in self._albums.items():
			print(v)


