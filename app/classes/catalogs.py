import abc
from app.common_definitions.helper_functions import convert_date_time_to_epoch as to_epoch


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
        self.db = database
        # private variable convention in python have '_' prefix
        self._books = {}

    def get_all(self):
        return self._books

    def get(self, id):
        return self._books[id]

    def modify(self, modified_book):
        modify_book_query = 'UPDATE book SET author = ?, title = ?, format = ?, pages = ?, publisher = ?, year_of_publication = ?' \
            ', language = ?, isbn_10 = ?, isbn_13 = ? WHERE id = ? '
        tuple_for_modify_query = (modified_book._author, modified_book._title, modified_book._format, modified_book._pages, modified_book._publisher,
                                  modified_book._year_of_publication, modified_book._language, modified_book._ISBN10, modified_book._ISBN13, modified_book._id)
        self.db.execute_query_write(modify_book_query, tuple_for_modify_query)
        self._books[int(modified_book.get_id())] = modified_book

    def add(self, book, add_to_db):
        # can act as a modify too!

        if add_to_db is True:
            insert_new_book_query = 'INSERT INTO book(author,title,format,pages,publisher,year_of_publication,language,isbn_10,isbn_13)' \
                'VALUES(?,?,?,?,?,?,?,?,?)'
            tuple_for_insert_query = (book._author, book._title, book._format, book._pages,
                                      book._publisher, book._year_of_publication, book._language, book._ISBN10, book._ISBN13)

            # getting the id of the last inserted book
            new_book_id = self.db.execute_query_write(
                insert_new_book_query, tuple_for_insert_query).lastrowid
            # since the object created has by default id = 0, we have to set
            # its id to the id obtained above
            book._id = new_book_id
            self._books[new_book_id] = book

        else:
            self._books[book._id] = book

    def remove(self, id):
        remove_book = 'DELETE FROM book WHERE id = ?'
        # the comma after id is because the execute query from sqlite takes
        # only tuples as second parameters
        self.db.execute_query_write(remove_book, (id,))
        return self._books.pop(id, None)

    def return_copies(self, id):
        return_records = 'SELECT * FROM book_copies WHERE id = ?'

    def display(self):

        for k, v in self._books.items():
            print(v)


class MovieCatalog(Catalog):

    def __init__(self, database):
        self.db = database
        self._movies = {}

    def get_all(self):
        return self._movies

    def get(self, id):
        return self._movies[id]

    def add(self, movie, add_to_db):

        if add_to_db is True:
            insert_new_movie_query = 'INSERT INTO movie(title, director, producers, actors, language, subtitles, dubbed, release_date, run_time)' \
                'VALUES(?,?,?,?,?,?,?,?,?)'
            tuple_for_insert_query = (movie._title, movie._director, movie._producers, movie._actors,
                                      movie._language, movie._subtitles, movie._dubbed, to_epoch(movie._release_date), movie._runtime)

            # getting the id of the last inserted movie
            new_movie_id = self.db.execute_query_write(
                insert_new_movie_query, tuple_for_insert_query).lastrowid
            # since the object created has by default id = 0, we have to set
            # its id to the id obtained above
            movie._id = new_movie_id
            self._movies[new_movie_id] = movie

        else:
            self._movies[movie._id] = movie

    def modify(self, modified_movie):

        modify_movie_query = 'UPDATE movie SET title = ?, director = ?, producers = ?, actors = ?, language = ?, subtitles = ?' \
            ', dubbed = ?, release_date = ?, run_time = ? WHERE id = ?'
        tuple_for_modify_query = (modified_movie._title, modified_movie._director, modified_movie._producers, modified_movie._actors, modified_movie._language,
                                  modified_movie._subtitles, modified_movie._dubbed, to_epoch(modified_movie._release_date), modified_movie._runtime, modified_movie._id)
        self.db.execute_query_write(modify_movie_query, tuple_for_modify_query)
        self._movies[int(modified_movie.get_id())] = modified_movie

    def remove(self, id):
        remove_movie = 'DELETE FROM movie WHERE id = ?'
        # the comma after id is because the execute query from sqlite takes
        # only tuples as second parameters
        self.db.execute_query_write(remove_movie, (id,))
        return self._movies.pop(id, None)

    def display(self):

        for k, v in self._movies.items():
            print(v)


class MagazineCatalog(Catalog):

    def __init__(self, database):
        self.db = database
        self._magazines = {}

    def get_all(self):
        return self._magazines

    def get(self, id):
        return self._magazines[id]

    def add(self, magazine, add_to_db):
        if add_to_db is True:

            insert_new_magazine_query = 'INSERT INTO magazine(title, publisher, year_of_publication, language, isbn_10, isbn_13)' \
                'VALUES(?,?,?,?,?,?)'
            tuple_for_insert_query = (magazine._title, magazine._publisher, magazine._year_of_publication,
                                      magazine._language, magazine._ISBN10, magazine._ISBN13)

            # getting the id of the last inserted magazine
            new_magazine_id = self.db.execute_query_write(
                insert_new_magazine_query, tuple_for_insert_query).lastrowid
            # since the object created has by default id = 0, we have to set
            # its id to the id obtained above
            magazine._id = new_magazine_id
            self._magazines[new_magazine_id] = magazine

        else:
            self._magazines[magazine._id] = magazine

    def modify(self, modified_magazine):
        modify_magazine_query = 'UPDATE magazine SET title = ?, publisher = ?, year_of_publication = ?, language = ?, isbn_10 = ?, isbn_13 = ?' \
            'WHERE id = ? '
        tuple_for_modify_query = (modified_magazine._title, modified_magazine._publisher, modified_magazine._year_of_publication,
                                  modified_magazine._language, modified_magazine._ISBN10, modified_magazine._ISBN13, modified_magazine._id)
        self.db.execute_query_write(
            modify_magazine_query, tuple_for_modify_query)
        self._magazines[int(modified_magazine.get_id())] = modified_magazine

    def remove(self, id):
        remove_magazine = 'DELETE FROM magazine WHERE id = ?'
        # the comma after id is because the execute query from sqlite takes
        # only tuples as second parameters
        self.db.execute_query_write(remove_magazine, (id,))
        return self._magazines.pop(id, None)

    def display(self):

        for k, v in self._magazines.items():
            print(v)


class AlbumCatalog(Catalog):

    def __init__(self, database):
        self.db = database
        self._albums = {}

    def get_all(self):
        return self._albums

    def get(self, id):
        return self._albums[id]

    def add(self, album, add_to_db):

        if add_to_db is True:
            insert_new_album = 'INSERT INTO album(type, title, artist, label, release_date, asin) VALUES(?,?,?,?,?,?)'
            tuple_for_insert_query = (
                album._type, album._title, album._artist, album._label, to_epoch(album._release_date), album._ASIN)

            # getting the id of the last inserted album
            new_album_id = self.db.execute_query_write(
                insert_new_album, tuple_for_insert_query).lastrowid
            # since the object created has by default id = 0, we have to set
            # its id to the id obtained above
            album._id = new_album_id
            self._albums[new_album_id] = album

        else:
            self._albums[album._id] = album

    def modify(self, modified_album):
        modify_album_query = 'UPDATE album SET type = ? , title = ?, artist = ?, label = ?, release_date = ?, asin = ? WHERE id = ?'
        tuple_for_modify_query = (modified_album._type, modified_album._title, modified_album._artist,
                                  modified_album._label, to_epoch(modified_album._release_date), modified_album._ASIN, int(modified_album._id))
        self.db.execute_query_write(modify_album_query, tuple_for_modify_query)
        self._albums[int(modified_album.get_id())] = modified_album

    def remove(self, id):
        remove_album = 'DELETE FROM album WHERE id = ?'
        # the comma after id is because the execute query from sqlite takes
        # only tuples as second parameters
        self.db.execute_query_write(remove_album, (id,))
        return self._albums.pop(id, None)

    def display(self):

        for k, v in self._albums.items():
            print(v)
