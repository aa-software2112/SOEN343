import abc


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

    def add(self, book):
        # can act as a modify too!
        self._books[book.get_id()] = book

    def remove(self, id):
        return self._books.pop(id, None)


class MovieCatalog(Catalog):

    def __init__(self):
        self._movies = {}

    def get_all(self):
        return self._movies

    def get(self, id):
        return self._movies[id]

    def add(self, movie):
        self._movies[movie.get_id()] = movie

    def remove(self, id):
        return self._movies.pop(id, None)


class MagazineCatalog(Catalog):

    def __init__(self):
        self._magazines = {}

    def get_all(self):
        return self._magazines

    def get(self, id):
        return self._magazines[id]

    def add(self, magazine):
        self._magazines[magazine.get_id()] = magazine

    def remove(self, id):
        return self._magazines.pop(id, None)


class AlbumCatalog(Catalog):

    def __init__(self):
        self._albums = {}

    def get_all(self):
        return self._albums

    def get(self, id):
        return self._albums[id]

    def add(self, album):
        self._albums[album.get_id()] = album

    def remove(self, id):
        return self._albums.pop(id, None)



