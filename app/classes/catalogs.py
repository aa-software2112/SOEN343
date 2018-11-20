import abc
from app.common_definitions.helper_functions import convert_date_time_to_epoch as to_epoch
from app.common_definitions.helper_functions import search_catalog
from app.common_definitions import helper_functions
from app.common_definitions.helper_functions import sort_records
from app.controllers.client_controller import ClientController
from app.classes.book import Book
from app.classes.movie import Movie
from app.classes.magazine import Magazine
from app.classes.album import Album
from app.classes.database_container import DatabaseContainer
from app.classes.lock import ReadWriteLock

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
    def add(self, object, add_to_db):
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

    @abc.abstractmethod
    def search(self, search_string):
        """ This method searches for an object in the collection and returns a list of all matches """
        pass


# Can be used to store either administrators or clients
class UserCatalog(Catalog):
    """
        This class does NOT use the Singleton pattern as
        multiple instances of this class may be created (due to there
        being an admin and client - two separate entities)
        """

    def __init__(self):

        self.db = DatabaseContainer.get_instance()
        self._users = {}
        self._rwl = ReadWriteLock()
        
    def get_all(self):
        self._rwl.start_read()
        temp = self._users
        self._rwl.end_read()
        return temp
        
    def get(self, id):
        self._rwl.start_read()
        temp = self._users[id]
        self._rwl.end_read()
        return temp
        
    def modify(self, modified_user):
        self._rwl.start_write()

        modify_user_query = 'UPDATE client SET firstName = ?, lastName = ?, physicalAddress = ?, email = ?, phoneNumber = ?, username = ?' \
            ', password = ?, isAdmin = ?, isLogged = ?, lastLogged = ? WHERE id = ?'
        tuple_for_modify_query = (modified_user._first_name, modified_user._last_name, modified_user._physical_address,
                                  modified_user._phone_number, modified_user._email, modified_user._username, modified_user._password,
                                  modified_user._is_admin, modified_user._is_logged, modified_user._last_logged,
                                  modified_user._id)

        self.db.execute_query_write(modify_user_query, tuple_for_modify_query)
        self._users[int(modified_user.get_id())] = modified_user

        self._rwl.end_write()

    def add(self, user, add_to_db):
        self._rwl.start_write()

        if add_to_db is True:

           
                insert_new_user_query = 'INSERT INTO client(firstName,lastName,physicalAddress,email,phoneNumber,username,password,isAdmin,isLogged,lastLogged)' \
                                        'VALUES(?,?,?,?,?,?,?,?,?,?)'
                tuple_for_insert_query = (user._first_name, user._last_name, user._physical_address,
                                  user._email, user._phone_number,  user._username, user._password,
                                  user._is_admin, user._is_logged, user._last_logged)

                # getting the id of the last inserted book
                new_book_id = self.db.execute_query_write(insert_new_user_query, tuple_for_insert_query).lastrowid
                # since the object created has by default id = 0, we have to set
                # its id to the id obtained above
                user._id = new_book_id
                self._users[new_book_id] = user

        else:
            self._users[user._id] = user

        self._rwl.end_write()

    def remove(self, id):
        self._rwl.start_write()
        remove_user = 'DELETE FROM client WHERE id = ?'
        # the comma after id is because the execute query from sqlite takes
        # only tuples as second parameters
        self.db.execute_query_write(remove_user, (id,))
        temp = self._users.pop(id, None)
        self._rwl.end_write()
        return temp

    def search(self, search_string):
        self._rwl.start_read()
        temp = search_catalog(self._users, search_string)
        self._rwl.end_read()
        return temp

class BookCatalog(Catalog):
    """
        This class uses the Singleton pattern.
        """
    _instance = None

    Filters = {"Author":"_author",
                "Title":"_title",
                "Publisher":"_publisher",
                "Language":"_language"
               }

    Sorts = {"Ascending Author":"_author",
             "Descending Author": "_author",
             "Ascending Title": "_title",
             "Descending Title": "_title",
             "Ascending Publisher":"_publisher",
             "Descending Publisher": "_publisher",
             "Ascending Year":"_year_of_publication",
             "Descending Year":"_year_of_publication"
             }

    @staticmethod
    def get_instance():
        """ Static access method. """
        if BookCatalog._instance is None:
            BookCatalog._instance = BookCatalog()
        return BookCatalog._instance

    def __init__(self):
        if BookCatalog._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            BookCatalog._instance = self
            self.db = DatabaseContainer.get_instance()
            # private variable convention in python have '_' prefix
            self._books = {}
            self._rwl = ReadWriteLock()

    def get_all(self):
        self._rwl.start_read()
        temp = self._books
        self._rwl.end_read()
        return temp

    def get(self, id):
        self._rwl.start_read()
        temp = self._books[id]
        self._rwl.end_read()
        return temp

    def modify(self, modified_book):
        self._rwl.start_write()
        modify_book_query = 'UPDATE book SET author = ?, title = ?, format = ?, pages = ?, publisher = ?, year_of_publication = ?' \
            ', language = ?, isbn_10 = ?, isbn_13 = ? WHERE id = ? '
        tuple_for_modify_query = (modified_book._author, modified_book._title, modified_book._format, modified_book._pages, modified_book._publisher,
                                  modified_book._year_of_publication, modified_book._language, modified_book._ISBN10, modified_book._ISBN13, modified_book._id)
        self.db.execute_query_write(modify_book_query, tuple_for_modify_query)
        self._books[int(modified_book.get_id())] = modified_book
        self._rwl.end_write()

    def add(self, book, add_to_db):

        self._rwl.start_write()

        if add_to_db is True:

            #If book exist, gets cursor that holds id, total_quantity & quantity_available of a book from book table, by quering title and year of publication of the added book.
            #If book doesn't exist, use the None value returned to add new book (operation found below).
            select_id_query = 'SELECT id, total_quantity, quantity_available FROM book WHERE book.title = ? AND book.author = ?'
            tuple_for_get_id = (book._title, book._author)
            existing_book_id_cursor = self.db.execute_query(
            select_id_query, tuple_for_get_id)

            existing_book_id_fetched = existing_book_id_cursor.fetchone()


            #if book doesn't exist, add new book in first and second table
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

            #else already exist. Need to add new book in second table and update quantity of first table
            else:

                #get id and get and increment total_quantity and quantity_available
                book._id = existing_book_id_fetched[0]
                book._total_quantity = existing_book_id_fetched[1] + 1
                book._quantity_available = existing_book_id_fetched[2] + 1
                #print(book._id , book._total_quantity, book._quantity_available)


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

        self._rwl.end_write()

    def get_copies(self, id):
        self._rwl.start_read()

        # get all copies of a selected book by ID. The query looks for all copies by referencing the book_id from the book-copy table to the id from book table.
        # Each copy is stored in a book object and has the same attributes as the original book (main table) with its own id as an exception, 'book_copy.id'.
        found_records = []
        get_book_records_by_id_tuple = (id,)
        get_book_records_query = """ SELECT book_copy.id, book.author, book.title, book.format, book.pages, book.publisher, book.year_of_publication, book.language, book.isbn_10, book.isbn_13 FROM book_copy INNER JOIN book ON book.id = book_copy.book_id WHERE book_copy.book_id = ?"""
        get_records_cursor = self.db.execute_query(get_book_records_query, get_book_records_by_id_tuple)

        all_records = get_records_cursor.fetchall()

        for row in all_records:
            found_records.append(Book(row))

        self._rwl.end_read()
        return found_records

    # 05/10/18 - This should probably be removed.
    def remove(self, id):
        self._rwl.start_write()
        remove_book = 'DELETE FROM book WHERE id = ?'
        # the comma after id is because the execute query from sqlite takes
        # only tuples as second parameters
        self.db.execute_query_write(remove_book, (id,))
        temp = self._books.pop(id, None)
        self._rwl.end_write()
        return temp

    def remove_copy(self, id):
        self._rwl.start_write()
        fetched_book = []
        get_id_tuple = (id,)

        # The ID from the paramater is a book copy ID. The JOIN statement in the query looks for the original book ID from the main table.
        # The query returns the original book ID, total quantity and the available quantuty.
        get_book_by_id_query = """ SELECT book.id, book.total_quantity, book.quantity_available FROM book_copy INNER JOIN book ON book.id = book_copy.book_id WHERE book_copy.id = ? """
        book_cursor = self.db.execute_query(get_book_by_id_query, get_id_tuple)
        fetched_book = book_cursor.fetchone()

        # Decrement the total_quantity and available_quantity by 1.
        # [Important] available_quantity is temporary. A restriction should handle the case where the quantity reaches 0.
        _id = fetched_book[0]
        _total_quantity = fetched_book[1] - 1
        _available_quantity = fetched_book[2] - 1

        # Remove the selected book from the book_copy table
        remove_book_query = """ DELETE FROM book_copy WHERE id = ? """
        self.db.execute_query_write(remove_book_query, get_id_tuple)

        # Update the total_quantity and available_quantity in the book table.
        update_book_quantity_query = """ UPDATE book SET total_quantity = ?, quantity_available = ? WHERE id = ? """
        update_book_quantity_tuple = (_total_quantity, _available_quantity, _id)
        self.db.execute_query_write(update_book_quantity_query, update_book_quantity_tuple)
        self._rwl.end_write()

    def display(self):

        for k, v in self._books.items():
            print(v)


    def search(self, search_string):
        self._rwl.start_read()
        temp = search_catalog(self._books, search_string)
        self._rwl.end_read()
        return temp

    def sort(self, sort_key_values, last_searched_list):
        self._rwl.start_read()
        # The sort_key_values is a string, not a dict

        transformed_sort_key_value = {}
        transformed_sort_key_value[sort_key_values.split(" ")[0].lower()] = self.Sorts[sort_key_values]
        temp = sort_records(transformed_sort_key_value, last_searched_list)
        self._rwl.end_read()
        return temp

    def filter(self, filter_key_values, last_searched_list):
        self._rwl.start_read()

        transformed_dict = {}

        for k, v in filter_key_values.items():

            # Converts the front-end key to a key representing the
            # attribute of the objects stored in this catalog
            transformed_dict[ self.Filters[k] ] = v

        temp = helper_functions.filter(transformed_dict, last_searched_list)
        self._rwl.end_read()

        return temp

    def set_available(self, book_copy_id):
        self._rwl.start_write()
        update_copy_query = 'UPDATE book_copy SET isLoaned = 0 WHERE id ?'
        self.db.execute_query_write(update_copy_query, (book_copy_id,))

        update_book_available = 'UPATE book SET quantity_available = quantity_available +1 INNER JOIN book ON book.id = book_copy.book_id WHERE book_copy.id = ?'
        self.db.execute_query_write(update_book_available,(book_copy_id,))
        self._rwl.end_write()


class MovieCatalog(Catalog):
    """
        This class uses the Singleton pattern.
        """
    _instance = None

    Filters = {"Director": "_director",
               "Title": "_title",
               "Producer": "_producers",
               "Actor": "_actors"
               }

    Sorts = {"Ascending Director":"_director",
             "Descending Director": "_director",
             "Ascending Title": "_title",
             "Descending Title": "_title",
             "Ascending Producer":"_producers",
             "Descending Producer": "_producers",
             "Ascending Runtime":"_runtime",
             "Descending Runtime":"_runtime"
             }

    @staticmethod
    def get_instance():
        """ Static access method. """
        if MovieCatalog._instance is None:
            MovieCatalog._instance = MovieCatalog()
        return MovieCatalog._instance

    def __init__(self):
        if MovieCatalog._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            MovieCatalog._instance = self
            self.db = DatabaseContainer.get_instance()
            self._movies = {}
            self._rwl = ReadWriteLock()

    def get_all(self):
        self._rwl.start_read()
        temp = self._movies
        self._rwl.end_read()
        return temp

    def get(self, id):
        self._rwl.start_read()
        temp = self._movies[id]
        self._rwl.end_read()
        return temp


    def add(self, movie, add_to_db):
        self._rwl.start_write()

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

        self._rwl.end_write()



    def modify(self, modified_movie):
        self._rwl.start_write()

        modify_movie_query = 'UPDATE movie SET title = ?, director = ?, producers = ?, actors = ?, language = ?, subtitles = ?' \
            ', dubbed = ?, release_date = ?, run_time = ? WHERE id = ?'
        tuple_for_modify_query = (modified_movie._title, modified_movie._director, modified_movie._producers, modified_movie._actors, modified_movie._language,
                                  modified_movie._subtitles, modified_movie._dubbed, to_epoch(modified_movie._release_date), modified_movie._runtime, modified_movie._id)
        self.db.execute_query_write(modify_movie_query, tuple_for_modify_query)
        self._movies[int(modified_movie.get_id())] = modified_movie

        self._rwl.end_write()

    def get_copies(self, id):
        self._rwl.start_read()

        # get all copies of a selected movie by ID. The query looks for all copies by referencing the movie_id from the movie-copy table to the id from movie table.
        # Each copy is stored in a movie object and has the same attributes as the original movie (main table) with its own id as an exception, 'movie_copy.id'.
        found_records = []
        get_movie_records_by_id_tuple = (id,)
        get_movie_records_query = """ SELECT movie_copy.id, movie.title, movie.director, movie.producers, movie.actors, movie.language, movie.subtitles, movie.dubbed, movie.release_date, movie.run_time FROM movie_copy INNER JOIN movie ON movie.id = movie_copy.movie_id WHERE movie_copy.movie_id = ? """
        get_records_cursor = self.db.execute_query(get_movie_records_query, get_movie_records_by_id_tuple)

        all_records = get_records_cursor.fetchall()

        for row in all_records:
            found_records.append(Movie(row))

        self._rwl.end_read()
        return found_records

    def remove(self, id):
        self._rwl.start_write()
        remove_movie = 'DELETE FROM movie WHERE id = ?'
        # the comma after id is because the execute query from sqlite takes
        # only tuples as second parameters
        self.db.execute_query_write(remove_movie, (id,))
        temp = self._movies.pop(id, None)
        self._rwl.end_write()
        return temp

    def remove_copy(self, id):
        self._rwl.start_write()
        fetched_movie = []
        get_id_tuple = (id,)

        # The ID from the paramater is a movie copy ID. The JOIN statement in the query looks for the original movie ID from the main table.
        # The query returns the original movie ID, total quantity and the available quantity.
        get_movie_by_id_query = """ SELECT movie.id, movie.total_quantity, movie.quantity_available FROM movie_copy INNER JOIN movie ON movie.id = movie_copy.movie_id WHERE movie_copy.id = ? """
        movie_cursor = self.db.execute_query(get_movie_by_id_query, get_id_tuple)
        fetched_movie = movie_cursor.fetchone()

        # Decrement the total_quantity and available_quantity by 1.
        _id = fetched_movie[0]
        _total_quantity = fetched_movie[1] - 1
        _available_quantity = fetched_movie[2] - 1

        # Remove the selected movie from the movie_copy table
        remove_movie_copy_query = """ DELETE FROM movie_copy WHERE id = ? """
        self.db.execute_query_write(remove_movie_copy_query, get_id_tuple)

        # Update the total_quantity and available_quantity in the movie table.
        update_movie_quantity_query = """ UPDATE movie SET total_quantity = ?, quantity_available = ? WHERE id = ? """
        update_movie_quantity_tuple = (_total_quantity, _available_quantity, _id)

        self.db.execute_query_write(update_movie_quantity_query, update_movie_quantity_tuple)

        self._rwl.end_write()

    def display(self):

        for k, v in self._movies.items():
            print(v)

    def search(self, search_string):
        self._rwl.start_read()
        temp = search_catalog(self._movies, search_string)
        self._rwl.end_read()
        return temp

    def sort(self, sort_key_values, last_searched_list):
        self._rwl.start_read()
        # The sort_key_values is a string, not a dict

        transformed_sort_key_value = {}

        transformed_sort_key_value[sort_key_values.split(" ")[0].lower()] = self.Sorts[sort_key_values]

        temp = sort_records(transformed_sort_key_value, last_searched_list)
        self._rwl.end_read()
        return temp

    def filter(self, filter_key_values, last_searched_list):
        self._rwl.start_read()

        transformed_dict = {}

        for k, v in filter_key_values.items():

            # Converts the front-end key to a key representing the
            # attribute of the objects stored in this catalog
            transformed_dict[ self.Filters[k] ] = v

        temp = helper_functions.filter(transformed_dict, last_searched_list)
        self._rwl.end_read()
        return temp

    def set_available(self, movie_copy_id):
        self._rwl.start_write()
        update_copy_query = 'UPDATE movie_copy SET isLoaned = 0 WHERE id ?'
        self.db.execute_query_write(update_copy_query, (movie_copy_id,))

        update_book_available = 'UPATE movie SET quantity_available = quantity_available +1 INNER JOIN movie ON movie.id = movie_copy.movie_id WHERE movie_copy.id = ?'
        self.db.execute_query_write(update_book_available, (movie_copy_id,))
        self._rwl.end_write()

class MagazineCatalog(Catalog):
    """
        This class uses the Singleton pattern.
        """
    _instance = None

    Filters = {"Title": "_title",
               "Publisher": "_publisher",
               "Language": "_language"
               }

    Sorts = {"Ascending Title": "_title",
             "Descending Title": "_title",
             "Ascending Publisher":"_publisher",
             "Descending Publisher": "_publisher",
             "Ascending Year":"_year_of_publication",
             "Descending Year":"_year_of_publication"
             }

    @staticmethod
    def get_instance():
        """ Static access method. """
        if MagazineCatalog._instance is None:
            MagazineCatalog._instance = MagazineCatalog()
        return MagazineCatalog._instance

    def __init__(self):
        if MagazineCatalog._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            MagazineCatalog._instance = self
            self.db = DatabaseContainer.get_instance()
            self._magazines = {}
            self._rwl = ReadWriteLock()

    def get_all(self):
        self._rwl.start_read()
        temp = self._magazines
        self._rwl.end_read()
        return temp

    def get(self, id):
        self._rwl.start_read()
        temp = self._magazines[id]
        self._rwl.end_read()
        return temp

    def add(self, magazine, add_to_db):
        self._rwl.start_write()

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
                insert_new_magazine_copy_query = 'INSERT INTO magazine_copy(magazine_id)' \
                'VALUES(?)'
                tuple_for_insert_copy_query = (new_magazine_id,)
                self.db.execute_query_write(insert_new_magazine_copy_query, tuple_for_insert_copy_query)

            #else already exist. Need to add new magazine in second table and update quantity of first table
            else:

                #get id and get and increment total_quantity and quantity_available
                magazine._id = existing_magazine_id_fetched[0]
                magazine._total_quantity = existing_magazine_id_fetched[1] + 1
                magazine._quantity_available = existing_magazine_id_fetched[2] + 1
                #print(magazine._id , magazine._total_quantity, magazine._quantity_available)


                #insert magazine into magazine_copy table
                insert_new_magazine_copy_query = 'INSERT INTO magazine_copy(magazine_id)' \
                'VALUES(?)'
                tuple_for_insert_copy_query =(magazine._id, )
                self.db.execute_query_write(insert_new_magazine_copy_query, tuple_for_insert_copy_query)

                #update magazine quantity in database
                update_new_magazine_quantity_query = 'UPDATE magazine SET total_quantity = ?, quantity_available = ? WHERE id = ?'
                tuple_for_updated_quantity_query = (magazine._total_quantity, magazine._quantity_available, magazine._id)
                update_magazine_quantity = self.db.execute_query_write(
                update_new_magazine_quantity_query, tuple_for_updated_quantity_query)

        else:
            self._magazines[magazine._id] = magazine

        self._rwl.end_write()


    def modify(self, modified_magazine):
        self._rwl.start_write()
        modify_magazine_query = 'UPDATE magazine SET title = ?, publisher = ?, year_of_publication = ?, language = ?, isbn_10 = ?, isbn_13 = ?' \
            'WHERE id = ? '
        tuple_for_modify_query = (modified_magazine._title, modified_magazine._publisher, modified_magazine._year_of_publication,
                                  modified_magazine._language, modified_magazine._ISBN10, modified_magazine._ISBN13, modified_magazine._id)
        self.db.execute_query_write(
            modify_magazine_query, tuple_for_modify_query)
        self._magazines[int(modified_magazine.get_id())] = modified_magazine
        self._rwl.end_write()

    def get_copies(self, id):
        self._rwl.start_read()

        found_records = []
        get_magazine_records_by_id_tuple = (id,)
        get_magazine_records_query = """ SELECT magazine_copy.id, magazine.title, magazine.publisher, magazine.year_of_publication, magazine.language, magazine.isbn_10, magazine.isbn_13 FROM magazine_copy INNER JOIN magazine ON magazine.id = magazine_copy.magazine_id WHERE magazine_copy.magazine_id = ? """
        get_records_cursor = self.db.execute_query(get_magazine_records_query, get_magazine_records_by_id_tuple)

        all_records = get_records_cursor.fetchall()

        for row in all_records:
            found_records.append(Magazine(row))
        self._rwl.end_read()
        return found_records

    def remove(self, id):
        self._rwl.start_write()
        remove_magazine = 'DELETE FROM magazine WHERE id = ?'
        # the comma after id is because the execute query from sqlite takes
        # only tuples as second parameters
        self.db.execute_query_write(remove_magazine, (id,))
        temp = self._magazines.pop(id, None)
        self._rwl.end_write()
        return temp

    def remove_copy(self, id):
        self._rwl.start_write()
        fetched_magazine = []
        get_id_tuple = (id,)

        # The ID from the paramater is a magazine copy ID. The JOIN statement in the query looks for the original magazine ID from the main table.
        # The query returns the original magazine ID, total quantity and the available quantity.
        get_magazine_by_id_query = """ SELECT magazine.id, magazine.total_quantity, magazine.quantity_available FROM magazine_copy INNER JOIN magazine ON magazine.id = magazine_copy.magazine_id WHERE magazine_copy.id = ? """
        magazine_cursor = self.db.execute_query(get_magazine_by_id_query, get_id_tuple)
        fetched_magazine = magazine_cursor.fetchone()

        # Decrement the total_quantity and available_quantity by 1.
        _id = fetched_magazine[0]
        _total_quantity = fetched_magazine[1] - 1
        _available_quantity = fetched_magazine[2] - 1

        # Remove the selected magazine from the movie_copy table
        remove_magazine_copy_query = """ DELETE FROM magazine_copy WHERE id = ? """
        self.db.execute_query_write(remove_magazine_copy_query, get_id_tuple)

        # Update the total_quantity and available_quantity in the magazine table.
        update_magazine_quantity_query = """ UPDATE magazine SET total_quantity = ?, quantity_available = ? WHERE id = ? """
        update_magazine_quantity_tuple = (_total_quantity, _available_quantity, _id)

        self.db.execute_query_write(update_magazine_quantity_query, update_magazine_quantity_tuple)

        self._rwl.end_write()

    def display(self):

        for k, v in self._magazines.items():
            print(v)

    def search(self, search_string):
        self._rwl.start_read()

        temp = search_catalog(self._magazines, search_string)
        self._rwl.end_read()
        return temp

    def sort(self, sort_key_values, last_searched_list):
        self._rwl.start_read()
        # The sort_key_values is a string, not a dict

        transformed_sort_key_value = {}

        transformed_sort_key_value[sort_key_values.split(" ")[0].lower()] = self.Sorts[sort_key_values]

        temp = sort_records(transformed_sort_key_value, last_searched_list)
        self._rwl.end_read()
        return temp

    def filter(self, filter_key_values, last_searched_list):
        self._rwl.start_read()

        transformed_dict = {}

        for k, v in filter_key_values.items():

            # Converts the front-end key to a key representing the
            # attribute of the objects stored in this catalog
            transformed_dict[ self.Filters[k] ] = v

        temp = helper_functions.filter(transformed_dict, last_searched_list)
        self._rwl.end_read()
        return temp



class AlbumCatalog(Catalog):
    """
        This class uses the Singleton pattern.
        """
    _instance = None

    Filters = {"Title": "_title",
               "Artist": "_artist",
               "Label": "_label"
               }

    Sorts = {"Ascending Title": "_title",
             "Descending Title": "_title",
             "Ascending Artist":"_artist",
             "Descending Artist": "_artist",
             "Ascending Label":"_label",
             "Descending Label":"_label"
             }

    @staticmethod
    def get_instance():
        """ Static access method. """
        if AlbumCatalog._instance is None:
            AlbumCatalog._instance = AlbumCatalog()
        return AlbumCatalog._instance

    def __init__(self):
        if AlbumCatalog._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            AlbumCatalog._instance = self
            self.db = DatabaseContainer.get_instance()
            self._albums = {}
            self._rwl = ReadWriteLock()

    def get_all(self):
        self._rwl.start_read()
        temp = self._albums
        self._rwl.end_read()
        return temp

    def get(self, id):
        self._rwl.start_read()
        temp = self._albums[id]
        self._rwl.end_read()
        return temp

    def add(self, album, add_to_db):
        self._rwl.start_write()

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
                new_album_id = self.db.execute_query_write(insert_new_album_query, tuple_for_insert_query).lastrowid
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

        self._rwl.end_write()


    def modify(self, modified_album):
        self._rwl.start_write()

        modify_album_query = 'UPDATE album SET type = ? , title = ?, artist = ?, label = ?, release_date = ?, asin = ? WHERE id = ?'
        tuple_for_modify_query = (modified_album._type, modified_album._title, modified_album._artist,
                                  modified_album._label, to_epoch(modified_album._release_date), modified_album._ASIN, int(modified_album._id))
        self.db.execute_query_write(modify_album_query, tuple_for_modify_query)
        self._albums[int(modified_album.get_id())] = modified_album

        self._rwl.end_write()

    def get_copies(self, id):
        self._rwl.start_read()

        # get all copies of a selected album by ID. The query looks for all copies by referencing the album_id from the album-copy table to the id from album table.
        # Each copy is stored in a album object and has the same attributes as the original album (main table) with its own id as an exception, 'album_copy.id'.
        found_records = []
        get_album_records_by_id_tuple = (id,)
        get_album_records_query = """ SELECT album_copy.id, album.type, album.title, album.artist, album.label, album.release_date, album.asin FROM album, album_copy WHERE album.id = ? AND album.id = album_copy.album_id"""
        get_copies_cursor = self.db.execute_query(get_album_records_query, get_album_records_by_id_tuple)

        all_records = get_copies_cursor.fetchall()

        for row in all_records:
            found_records.append(Album(row))
        self._rwl.end_read()
        return found_records

    def remove(self, id):
        self._rwl.start_write()
        remove_album = 'DELETE FROM album WHERE id = ?'
        # the comma after id is because the execute query from sqlite takes
        # only tuples as second parameters
        self.db.execute_query_write(remove_album, (id,))
        temp = self._albums.pop(id, None)
        self._rwl.end_write()
        return temp

    def remove_copy(self, id):
        self._rwl.start_write()
        fetched_album = []
        get_id_tuple = (id,)

        # The ID from the paramater is a album copy ID. The JOIN statement in the query looks for the original album ID from the main table.
        # The query returns the original album ID, total quantity and the available quantity.
        get_album_by_id_query = """ SELECT album.id, album.total_quantity, album.quantity_available FROM album_copy INNER JOIN album ON album.id = album_copy.album_id WHERE album_copy.id = ? """
        album_cursor = self.db.execute_query(get_album_by_id_query, get_id_tuple)
        fetched_album = album_cursor.fetchone()

        # Decrement the total_quantity and available_quantity by 1.
        _id = fetched_album[0]
        _total_quantity = fetched_album[1] - 1
        _available_quantity = fetched_album[2] - 1

        # Remove the selected album from the movie_copy table
        remove_album_copy_query = """ DELETE FROM album_copy WHERE id = ? """
        self.db.execute_query_write(remove_album_copy_query, get_id_tuple)

        # Update the total_quantity and available_quantity in the magazine table.
        update_album_quantity_query = """ UPDATE album SET total_quantity = ?, quantity_available = ? WHERE id = ? """
        update_album_quantity_tuple = (_total_quantity, _available_quantity, _id)

        self.db.execute_query_write(update_album_quantity_query, update_album_quantity_tuple)

        self._rwl.end_write()

    def display(self):

        for k, v in self._albums.items():
            print(v)

    def search(self, search_string):
        self._rwl.start_read()

        temp = search_catalog(self._albums, search_string)

        self._rwl.end_read()
        return temp

    def sort(self, sort_key_values, last_searched_list):
        self._rwl.start_read()
        # The sort_key_values is a string, not a dict

        transformed_sort_key_value = {}

        transformed_sort_key_value[sort_key_values.split(" ")[0].lower()] = self.Sorts[sort_key_values]

        temp = sort_records(transformed_sort_key_value, last_searched_list)
        self._rwl.end_read()
        return temp

    def filter(self, filter_key_values, last_searched_list):
        self._rwl.start_read()

        transformed_dict = {}

        for k, v in filter_key_values.items():

            # Converts the front-end key to a key representing the
            # attribute of the objects stored in this catalog
            transformed_dict[ self.Filters[k] ] = v

        temp = helper_functions.filter(transformed_dict, last_searched_list)
        self._rwl.end_read()
        return temp

    def set_available(self, album_copy_id):
        self._rwl.start_write()
        update_copy_query = 'UPDATE album_copy SET isLoaned = 0 WHERE id ?'
        self.db.execute_query_write(update_copy_query, (album_copy_id,))

        update_book_available = 'UPATE album SET quantity_available = quantity_available +1 INNER JOIN album ON album.id = album_copy.album_id WHERE album_copy.id = ?'
        self.db.execute_query_write(update_book_available, (album_copy_id,))
        self._rwl.end_write()

class LoanCatalog(Catalog):
    """
    This class uses the Singleton pattern.
    """
    _instance = None

    Filters = { }

    Sorts = { }

    @staticmethod
    def get_instance():
        """ Static access method. """
        if LoanCatalog._instance is None:
            LoanCatalog._instance = LoanCatalog()
        return LoanCatalog._instance

    def __init__(self):
        """
        This initializer creates all the catalogs necessary
        for making loans appropriately; setting a loan to "returned" should
        return the copy
        """

        if LoanCatalog._instance is not None:

            raise Exception("This class is a singleton!")

        else:

            # Catalogs necessary for making and returning loans
            self.book_catalog = BookCatalog.get_instance()
            self.album_catalog = AlbumCatalog.get_instance()
            self.movie_catalog = MovieCatalog.get_instance()
            self.client_controller = ClientController.get_instance()

            LoanCatalog._instance = self
            self.db = DatabaseContainer.get_instance()
            self._loans = {}
            self._rwl = ReadWriteLock()


    def get_all(self):
        self._rwl.start_read()
        temp = self._loans
        self._rwl.end_read()

    def get(self, id):
        self._rwl.start_read()
        temp = self._loans[id]
        self._rwl.end_read()
        return temp

    def add(self, loan_obj, add_to_db):
        self._rwl.start_write()

        if add_to_db is True:

            # Add the object into the database
            # Note; all *_time attributes were set before the call to this method was made
            insert_new_loan_query = 'INSERT INTO loan(user_id, record_id, table_name, loan_time, due_time, return_time, is_returned)' \
            'VALUES(?,?,?,?,?,?,?)'


            tuple_for_insert_query = (loan_obj._user_id, loan_obj._record_id, loan_obj._table_name, loan_obj._loan_time, loan_obj._due_time, \
                                      loan_obj._return_time, loan_obj._is_returned)

            # getting the id of the last inserted loan
            new_loan_id = self.db.execute_query_write(insert_new_loan_query, tuple_for_insert_query).lastrowid

            # since the object created has by default id = -1, we have to set
            # its id to that found in the database
            loan_obj.set_loan_id(new_loan_id)

            # Add the loan to the dictionary of loans
            self._loans[loan_obj.get_id()] = loan_obj

        else:
            self._loans[loan_obj.get_id()] = loan_obj
        self._rwl.end_write()



    def modify(self, modified_loan):
        self._rwl.start_write()
        """
        Modifies the values in the loan table
        :param modified_loan: The loan object with attributes to replace a previous one, based on
        the id property
        :return: N/A
        """

        print("Needs implementation")

        #modify_loans_query = 'UPDATE album SET type = ? , title = ?, artist = ?, label = ?, release_date = ?, asin = ? WHERE id = ?'
        #tuple_for_modify_query = (modified_album._type, modified_album._title, modified_album._artist,
        #                          modified_album._label, to_epoch(modified_album._release_date), modified_album._ASIN, int(modified_album._id))
        #self.db.execute_query_write(modify_album_query, tuple_for_modify_query)
        #self._albums[int(modified_album.get_id())] = modified_album
        self._rwl.end_write()

    def remove(self, id):
        self._rwl.start_write()
        """
        This function simply removes a loan from the list of loans; cannot remove
        the object if the item is still out as loaned!
        :param id: the id of the loan to remove
        :return: None if no object was removed, otherwise, object that was removed
        """

        loan = self._loans[id]

        # Loan was returned, OK to remove from database & memory
        if loan._is_returned == 1:

            remove_album = 'DELETE FROM loan WHERE id = ?'

            # Remove the loan from the database
            self.db.execute_query_write(remove_album, (id,))

            temp = self._loans.pop(id, None)

            self._rwl.end_write()

        self._rwl.end_write()
        return None

    def display(self):
        self._rwl.start_read()

        for k, v in self._loans.items():
            print(v)

        self._rwl.end_read()

    def search(self, search_string):

        search_list = []

        print("Implementation needed")

        return search_list

    def return_loaned_items(self, loan_id):
        loan = self.get(loan_id)
        loan.set_loan_as_returned()
        record_type = loan.get_table_name()

        if record_type == "book_copy":
            self.book_catalog.set_available(loan.get_record_id)

        elif record_type == "album_copy":
            self.album_catalog.set_available(loan.get_record_id)

        elif record_type == "movie_copy":
            self.movie_catalog.set_available(loan.get_record_id)


