import abc

# Abstract class Catalog
class Catalog(abc.ABC):

    @abc.abstractmethod
    def getAll(self):
        pass
    @abc.abstractmethod
    def get(self, id):
        pass
    @abc.abstractmethod
    def add(self, resource):
        pass
    @abc.abstractmethod
    def remove(self, id):
        pass

class BookCatalog(Catalog):

    def __init__(self):
        # private variable convention in python have '_' prefix
        self._books = {}

    def getAll(self):
        return self._books

    def get(self, id):
        return self._books[id]

    def add(self, book):
        # can act as a modify too!
        self._books[book.getId()] = book

    def remove(self, id):
        return self._books.pop(id, None)

class MovieCatalog(Catalog):

    def __init__(self):
        self._movies = {}

    def getAll(self):
        return self._movies

    def get(self, id):
        return self._movies[id]

    def add(self, movie):
        self._movies[movie.getId()] = movie

    def remove(self, id):
        return self._movies.pop(id, None)

class MagazineCatalog(Catalog):

    def __init__(self):
        self._magazines = {}

    def getAll(self):
        return self._magazines

    def get(self, id):
        return self._magazines[id]

    def add(self, magazine):
        self._magazines[magazine.getId()] = magazine

    def remove(self, id):
        return self._magazines.pop(id,None)

class AlbumCatalog(Catalog):

    def __init__(self):
        self._albums = {}

    def getAll(self):
        return self._albums

    def get(self, id):
        return self._albums[id]

    def add(self, album):
        self._albums[album.getId()] = album

    def remove(self, id):
        return self._albums.pop(id, None)



