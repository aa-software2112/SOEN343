import abc
from app.common_definitions.helper_functions import convert_date_time_to_epoch as to_epoch
from app.classes.book import Book
from app.classes.movie import Movie
from app.classes.magazine import Magazine
from app.classes.album import Album

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

        if add_to_db is True:
                 
            #If book exist, gets cursor that holds id, total_quantity & quantity_available of a book from book table, by quering title and year of publication of the added book.
            #If book doesn't exist, use the None value returned to add new book (operation found below).
            select_id_query = 'SELECT id, total_quantity, quantity_available FROM book WHERE book.title = ? AND book.author = ?'
            tuple_for_get_id = (book._title, book._author)
            existing_book_id_cursor = self.db.execute_query(
            select_id_query, tuple_for_get_id)
        
            existing_book_id_fetched = existing_book_id_cursor.fetchone()
          

            #if already exist, add new book in first and second table
            if existing_book_id_fetched is None:
               #insert book into book table
                insert_new_book_query = 'INSERT INTO book(author,title,format,pages,publisher,year_of_publication,language,isbn_10,isbn_13,total_quantity,quantity_available)' \
                'VALUES(?,?,?,?,?,?,?,?,?,?,?)'
                tuple_for_insert_query = (book._author, book._title, book._format, book._pages,
                                    book._publisher, book._year_of_publication, book._language, book._ISBN10, book._ISBN13, book._total_quantity, book._quantity_available)
                   
                # getting the id of the last inserted book
                new_book_id = self.db.execute_query_write(
                insert_new_book_query, tuple_for_insert_query).lastrowid
                # since the object created has by default id = 0, we have to set
                # its id to the id obtained above
                book._id = new_book_id
                self._books[new_book_id] = book
                    
                #insert book into book_copy table
                insert_new_book_copy_query = 'INSERT INTO book_copy(book_id, isLoaned)' \
                'VALUES(?,?)'
                tuple_for_insert_copy_query = (new_book_id, 0)
                self.db.execute_query_write(insert_new_book_copy_query, tuple_for_insert_copy_query)

            #else doesn't already exist. Need to add new book in second table and update quantity of first table
            else:
                
                #get id and get and increment total_quantity and quantity_available
                book._id = existing_book_id_fetched[0]
                book._total_quantity = existing_book_id_fetched[1] + 1
                book._quantity_available = existing_book_id_fetched[2] + 1
                print(book._id , book._total_quantity, book._quantity_available)
         

                #insert book into book_copy table
                insert_new_book_copy_query = 'INSERT INTO book_copy(book_id, isLoaned)' \
                'VALUES(?,?)'
                tuple_for_insert_copy_query =(book._id, 0)
                self.db.execute_query_write(insert_new_book_copy_query, tuple_for_insert_copy_query)
                
                #update book quantity in database
                update_new_book_quantity_query = 'UPDATE book SET total_quantity = ?, quantity_available = ? WHERE id = ?'
                tuple_for_updated_quantity_query = (book._total_quantity, book._quantity_available, book._id)
                update_book_quantity = self.db.execute_query_write(
                update_new_book_quantity_query, tuple_for_updated_quantity_query)

        else:
            self._books[book._id] = book



    def remove(self, id):
        remove_book = 'DELETE FROM book WHERE id = ?'
        # the comma after id is because the execute query from sqlite takes
        # only tuples as second parameters
        self.db.execute_query_write(remove_book, (id,))
        return self._books.pop(id, None)

    def get_copies(self, id):

        found_copies = []

        #get_copy_records_query = """ SELECT book_copy.id, book.author, book.title, book.format, book.pages, book.publisher, book.year_of_publication, book.language, book.isbn_10, book.isbn_13 FROM book, book_copy WHERE book.id = ? AND book.id = book_copy.book_id"""
        get_copy_records_query = """ SELECT book_copy.id, book.author, book.title, book.format, book.pages, book.publisher, book.year_of_publication, book.language, book.isbn_10, book.isbn_13 FROM book_copy INNER JOIN book ON book.id = book_copy.book_id WHERE book_copy.book_id = ?"""
        get_copies_cursor = self.db.execute_query(get_copy_records_query, (id,))

        copy_records = get_copies_cursor.fetchall()

        for row in copy_records:
            found_copies.append(Book(row))

        return found_copies

    def remove_copy(self, id):
        remove_book_copy = """ DELETE FROM book_copy WHERE id = ? """

        print("Deleting book with ID: " + str(id))
        self.db.execute_query_write(remove_book_copy, (id,))

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
                 
            #If movie exist, gets cursor that holds id, total_quantity & quantity_available of a movie from movie table, by quering title and year of publication of the added movie.
            #If movie doesn't exist, use the None value returned to add new movie (operation found below).
            select_id_query = 'SELECT id, total_quantity, quantity_available FROM movie WHERE movie.title = ? AND movie.run_time = ?'
            tuple_for_get_id = (movie._title, movie._runtime)
            existing_movie_id_cursor = self.db.execute_query(
            select_id_query, tuple_for_get_id)
        
            existing_movie_id_fetched = existing_movie_id_cursor.fetchone()
          

            #if movie doesn't already exist in first table, add new movie in first and second table
            if existing_movie_id_fetched is None:
               #insert movie into movie table
                insert_new_movie_query = 'INSERT INTO movie(title, director, producers, actors, language, subtitles, dubbed, release_date, run_time, total_quantity, quantity_available)' \
                'VALUES(?,?,?,?,?,?,?,?,?,?,?)'
                tuple_for_insert_query = (movie._title, movie._director, movie._producers, movie._actors,
                                      movie._language, movie._subtitles, movie._dubbed, to_epoch(movie._release_date), movie._runtime, movie._total_quantity, movie._quantity_available)
    
                # getting the id of the last inserted movie
                new_movie_id = self.db.execute_query_write(
                insert_new_movie_query, tuple_for_insert_query).lastrowid
                # since the object created has by default id = 0, we have to set
                # its id to the id obtained above
                movie._id = new_movie_id
                self._movies[new_movie_id] = movie
                    
                #insert movie into movie_copy table
                insert_new_movie_copy_query = 'INSERT INTO movie_copy(movie_id, isLoaned)' \
                'VALUES(?,?)'
                tuple_for_insert_copy_query = (new_movie_id, 0)
                self.db.execute_query_write(insert_new_movie_copy_query, tuple_for_insert_copy_query)

            #else already exist. Need to add new movie in second table and update quantity of first table
            else:
                
                #get id and get and increment total_quantity and quantity_available
                movie._id = existing_movie_id_fetched[0]
                movie._total_quantity = existing_movie_id_fetched[1] + 1
                movie._quantity_available = existing_movie_id_fetched[2] + 1
                print(movie._id , movie._total_quantity, movie._quantity_available)
         

                #insert movie into movie_copy table
                insert_new_movie_copy_query = 'INSERT INTO movie_copy(movie_id, isLoaned)' \
                'VALUES(?,?)'
                tuple_for_insert_copy_query =(movie._id, 0)
                self.db.execute_query_write(insert_new_movie_copy_query, tuple_for_insert_copy_query)
                
                #update movie quantity in database
                update_new_movie_quantity_query = 'UPDATE movie SET total_quantity = ?, quantity_available = ? WHERE id = ?'
                tuple_for_updated_quantity_query = (movie._total_quantity, movie._quantity_available, movie._id)
                update_movie_quantity = self.db.execute_query_write(
                update_new_movie_quantity_query, tuple_for_updated_quantity_query)

        else:
            self._movies[movie._id] = movie



    def modify(self, modified_movie):

        modify_movie_query = 'UPDATE movie SET title = ?, director = ?, producers = ?, actors = ?, language = ?, subtitles = ?' \
            ', dubbed = ?, release_date = ?, run_time = ? WHERE id = ?'
        tuple_for_modify_query = (modified_movie._title, modified_movie._director, modified_movie._producers, modified_movie._actors, modified_movie._language,
                                  modified_movie._subtitles, modified_movie._dubbed, to_epoch(modified_movie._release_date), modified_movie._runtime, modified_movie._id)
        self.db.execute_query_write(modify_movie_query, tuple_for_modify_query)
        self._movies[int(modified_movie.get_id())] = modified_movie
        
    def get_copies(self, id):

        found_copies = []

        get_copy_records_query = """ SELECT movie_copy.id, movie.title, movie.director, movie.producers, movie.actors, movie.language, movie.subtitles, movie.dubbed, movie.release_date, movie.run_time FROM movie, movie_copy WHERE movie.id = ? AND movie.id = movie_copy.movie_id"""
        get_copies_cursor = self.db.execute_query(get_copy_records_query, (id,))

        copy_records = get_copies_cursor.fetchall()

        for row in copy_records:
            found_copies.append(Movie(row))

        return found_copies

    def remove(self, id):
        remove_movie = 'DELETE FROM movie WHERE id = ?'
        # the comma after id is because the execute query from sqlite takes
        # only tuples as second parameters
        self.db.execute_query_write(remove_movie, (id,))
        return self._movies.pop(id, None)

    def remove_copy(self, id):
        remove_movie_copy = """ DELETE FROM movie_copy WHERE id = ? """

        self.db.execute_query_write(remove_movie_copy, (id,))

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
                 
            #If magazine exist, gets cursor that holds id, total_quantity & quantity_available of a magazine from magazine table, by quering title and year of publication of the added magazine.
            #If magazine doesn't exist, use the None value returned to add new magazine (operation found below).
            select_id_query = 'SELECT id, total_quantity, quantity_available FROM magazine WHERE magazine.title = ? AND magazine.year_of_publication = ?'
            tuple_for_get_id = (magazine._title, magazine._year_of_publication)
            existing_magazine_id_cursor = self.db.execute_query(
            select_id_query, tuple_for_get_id)
        
            existing_magazine_id_fetched = existing_magazine_id_cursor.fetchone()
          

            #if doesn't exist, add new magazine in first and second table
            if existing_magazine_id_fetched is None:
               #insert magazine into magazine table
                insert_new_magazine_query = 'INSERT INTO magazine(title, publisher, year_of_publication, language, isbn_10, isbn_13,total_quantity,quantity_available)' \
                'VALUES(?,?,?,?,?,?,?,?)'
                tuple_for_insert_query = (magazine._title, magazine._publisher, magazine._year_of_publication,
                                      magazine._language, magazine._ISBN10, magazine._ISBN13, magazine._total_quantity, magazine._quantity_available)
    
                # getting the id of the last inserted magazine
                new_magazine_id = self.db.execute_query_write(
                insert_new_magazine_query, tuple_for_insert_query).lastrowid
                # since the object created has by default id = 0, we have to set
                # its id to the id obtained above
                magazine._id = new_magazine_id
                self._magazines[new_magazine_id] = magazine
                    
                #insert magazine into magazine_copy table
                insert_new_magazine_copy_query = 'INSERT INTO magazine_copy(magazine_id, isLoaned)' \
                'VALUES(?,?)'
                tuple_for_insert_copy_query = (new_magazine_id, 0)
                self.db.execute_query_write(insert_new_magazine_copy_query, tuple_for_insert_copy_query)

            #else already exist. Need to add new magazine in second table and update quantity of first table
            else:
                
                #get id and get and increment total_quantity and quantity_available
                magazine._id = existing_magazine_id_fetched[0]
                magazine._total_quantity = existing_magazine_id_fetched[1] + 1
                magazine._quantity_available = existing_magazine_id_fetched[2] + 1
                print(magazine._id , magazine._total_quantity, magazine._quantity_available)
         

                #insert magazine into magazine_copy table
                insert_new_magazine_copy_query = 'INSERT INTO magazine_copy(magazine_id, isLoaned)' \
                'VALUES(?,?)'
                tuple_for_insert_copy_query =(magazine._id, 0)
                self.db.execute_query_write(insert_new_magazine_copy_query, tuple_for_insert_copy_query)
                
                #update magazine quantity in database
                update_new_magazine_quantity_query = 'UPDATE magazine SET total_quantity = ?, quantity_available = ? WHERE id = ?'
                tuple_for_updated_quantity_query = (magazine._total_quantity, magazine._quantity_available, magazine._id)
                update_magazine_quantity = self.db.execute_query_write(
                update_new_magazine_quantity_query, tuple_for_updated_quantity_query)

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

    def get_copies(self, id):

        found_copies = []

        get_copy_records_query = """ SELECT magazine_copy.id, magazine.title, magazine.publisher, magazine.year_of_publication, magazine.language, magazine.isbn_10, magazine.isbn_13 FROM magazine, magazine_copy WHERE magazine.id = ? AND magazine.id = magazine_copy.magazine_id"""
        get_copies_cursor = self.db.execute_query(get_copy_records_query, (id,))

        copy_records = get_copies_cursor.fetchall()

        for row in copy_records:
            found_copies.append(Magazine(row))

        return found_copies

    def remove(self, id):
        remove_magazine = 'DELETE FROM magazine WHERE id = ?'
        # the comma after id is because the execute query from sqlite takes
        # only tuples as second parameters
        self.db.execute_query_write(remove_magazine, (id,))
        return self._magazines.pop(id, None)

    def remove_copy(self, id):
        remove_magazine_copy = """ DELETE FROM magazine_copy WHERE id = ? """

        self.db.execute_query_write(remove_magazine_copy, (id,))

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
                 
            #If album exist, gets cursor that holds id, total_quantity & quantity_available of a album from album table, by quering title and asin of the added album.
            #If album doesn't exist, use the None value returned to add new album (operation found below).
            select_id_query = 'SELECT id, total_quantity, quantity_available FROM album WHERE album.title = ? AND album.artist = ?'
            tuple_for_get_id = (album._title, album._artist)
            existing_album_id_cursor = self.db.execute_query(
            select_id_query, tuple_for_get_id)
        
            existing_album_id_fetched = existing_album_id_cursor.fetchone()
          

            #if doesn't exist, add new album in first and second table
            if existing_album_id_fetched is None:
                #insert album into album table
                insert_new_album_query = 'INSERT INTO album(type, title, artist, label, release_date, asin, total_quantity, quantity_available)' \
                'VALUES(?,?,?,?,?,?,?,?)'
                tuple_for_insert_query = (album._type, album._title, album._artist, album._label, to_epoch(album._release_date), album._ASIN, album._total_quantity, album._quantity_available)

                # getting the id of the last inserted album
                new_album_id = self.db.execute_query_write(
                insert_new_album_query, tuple_for_insert_query).lastrowid
                # since the object created has by default id = 0, we have to set
                # its id to the id obtained above
                album._id = new_album_id
                self._albums[new_album_id] = album
                    
                #insert album into album_copy table
                insert_new_album_copy_query = 'INSERT INTO album_copy(album_id, isLoaned)' \
                'VALUES(?,?)'
                tuple_for_insert_copy_query = (new_album_id, 0)
                self.db.execute_query_write(insert_new_album_copy_query, tuple_for_insert_copy_query)

            #else already exist. Need to add new album in second table and update quantity of first table
            else:
                
                #get id and get and increment total_quantity and quantity_available
                album._id = existing_album_id_fetched[0]
                album._total_quantity = existing_album_id_fetched[1] + 1
                album._quantity_available = existing_album_id_fetched[2] + 1
                print(album._id , album._total_quantity, album._quantity_available)
         

                #insert album into album_copy table
                insert_new_album_copy_query = 'INSERT INTO album_copy(album_id, isLoaned)' \
                'VALUES(?,?)'
                tuple_for_insert_copy_query =(album._id, 0)
                self.db.execute_query_write(insert_new_album_copy_query, tuple_for_insert_copy_query)
                
                #update album quantity in database
                update_new_album_quantity_query = 'UPDATE album SET total_quantity = ?, quantity_available = ? WHERE id = ?'
                tuple_for_updated_quantity_query = (album._total_quantity, album._quantity_available, album._id)
                update_album_quantity = self.db.execute_query_write(
                update_new_album_quantity_query, tuple_for_updated_quantity_query)

        else:
            self._albums[album._id] = album
    
    
    def modify(self, modified_album):
        modify_album_query = 'UPDATE album SET type = ? , title = ?, artist = ?, label = ?, release_date = ?, asin = ? WHERE id = ?'
        tuple_for_modify_query = (modified_album._type, modified_album._title, modified_album._artist,
                                  modified_album._label, to_epoch(modified_album._release_date), modified_album._ASIN, int(modified_album._id))
        self.db.execute_query_write(modify_album_query, tuple_for_modify_query)
        self._albums[int(modified_album.get_id())] = modified_album

    def get_copies(self, id):

        found_copies = []

        get_copy_records_query = """ SELECT album_copy.id, album.type, album.title, album.artist, album.label, album.release_date, album.asin FROM album, album_copy WHERE album.id = ? AND album.id = album_copy.album_id"""
        get_copies_cursor = self.db.execute_query(get_copy_records_query, (id,))

        copy_records = get_copies_cursor.fetchall()

        for row in copy_records:
            found_copies.append(Album(row))

        return found_copies

    def remove(self, id):
        remove_album = 'DELETE FROM album WHERE id = ?'
        # the comma after id is because the execute query from sqlite takes
        # only tuples as second parameters
        self.db.execute_query_write(remove_album, (id,))
        return self._albums.pop(id, None)

    def remove_copy(self, id):
        remove_album_copy = """ DELETE FROM album_copy WHERE id = ? """

        self.db.execute_query_write(remove_album_copy, (id,))

    def display(self):

        for k, v in self._albums.items():
            print(v)