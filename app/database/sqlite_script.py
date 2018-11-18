import sqlite3
from sqlite3 import Error
from faker import Faker
from app.classes.catalogs import *
from app.classes.user import User

import time
import glob


def create_connection(database_file_path):
    """
    Function takes 'database_file_path' (exact path of database in your directory or path + name of database you wish to create. Please write it down in main method)
    and creates database connecton to SQLite database specified inside the database_file_path. Returns connection object 'conn'
    """
    try:
        conn = sqlite3.connect(database_file_path)
        return conn
    except Error as e:
        print(e)

    return None


def create_in_memory_connection():
    """
    Function creates SQLite database in memory
    if you wish to use a temporary database, use this function but if you wish to empty previous database, 
    simply delete the db file containing the database you wish to empty.
    """
    try:
        conn = sqlite3.connect(':memory:')
        return conn
    except Error as e:
        print(e)

    return None


def create_table(database, sql_create_x_table):
    """
    Function takes database connection object 'conb' and sql statement to create table 'sql_create_x_table'.  
    creates table inside database. 
    """
    try:
        c = database.connection.cursor()
        c.execute(sql_create_x_table)
    except Error as e:
        print(e)

def create_book_copy(database, book):
    """
    Function takes database connection object 'conn' and a book copy
    creates a new book copy into the book copy table
    """
    sql = ''' INSERT INTO book_copy(book_id,isLoaned)
              VALUES(?,?) '''
    database.execute_query_write(sql,book)

def create_magazine_copy(database, magazine):
    """
    Function takes database connection object 'conn' and a magazine copy
    creates a new magazine copy into the magazine copy table
    """
    sql = ''' INSERT INTO magazine_copy(magazine_id,isLoaned)
              VALUES(?,?) '''
    database.execute_query_write(sql, magazine)

def create_movie_copy(database, movie):
    """
    Function takes database connection object 'conn' and a movie copy
    creates a new movie copy into the movie copy table
    """
    sql = ''' INSERT INTO movie_copy(movie_id,isLoaned)
              VALUES(?,?) '''
    database.execute_query_write(sql, movie)

def create_album_copy(database, album):
    """
    Function takes database connection object 'conn' and a album copy
    creates a new album copy into the album copy table
    """
    sql = ''' INSERT INTO album_copy(album_id,isLoaned)
              VALUES(?,?) '''
    database.execute_query_write(sql, album)

def close_connection(conn):
    """
    Function takes database connection object 'conn'.
    closes connection to database (good practice)
    """
    try:
        conn.close()
    except Error as e:
        print(e)


def initializeAndFillDatabase(database, catalog_controller, client_controller, admin_controller):
    """
    Main where we implement most methods above (create connection, create table, insert data, close connection.)
    """

    # Database already exists; do nothing
    if len(glob.glob(database.dbPath)) == 1:
        return

    database.make_connection()
    # initialized variable with query that creates book table with columns/attributes
    sql_create_book_table = """CREATE TABLE IF NOT EXISTS book (
                                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                    author TEXT NOT NULL,
                                    title TEXT NOT NULL,
                                    format TEXT NOT NULL,
                                    pages INTEGER NOT NULL,
                                    publisher TEXT NOT NULL,
                                    year_of_publication INTEGER NOT NULL,
                                    language TEXT NOT NULL,
                                    isbn_10 TEXT NOT NULL,
                                    isbn_13 TEXT NOT NULL,
                                    total_quantity INTEGER NOT NULL,
                                    quantity_available INTEGER NOT NULL
                                );"""

    # initialized variable with query that creates magazine table with columns/attributes
    sql_create_magazine_table = """CREATE TABLE IF NOT EXISTS magazine (
                                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                    title TEXT NOT NULL,
                                    publisher TEXT NOT NULL,
                                    year_of_publication INTEGER NOT NULL,
                                    language TEXT NOT NULL,
                                    isbn_10 TEXT NOT NULL,
                                    isbn_13 TEXT NOT NULL,
                                    total_quantity INTEGER NOT NULL,
                                    quantity_available INTEGER NOT NULL
                                );"""

    # initialized variable with query that creates movie table with columns/attributes
    sql_create_movie_table = """CREATE TABLE IF NOT EXISTS movie (
                                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                    title TEXT NOT NULL,
                                    director TEXT NOT NULL,
                                    producers TEXT NOT NULL,
                                    actors TEXT NOT NULL,
                                    language TEXT NOT NULL,
                                    subtitles TEXT NOT NULL,
                                    dubbed TEXT NOT NULL,
                                    release_date INTEGER NOT NULL,
                                    run_time INTEGER NOT NULL,
                                    total_quantity INTEGER NOT NULL,
                                    quantity_available INTEGER NOT NULL
                                );"""

    # initialized variable with query that creates album table with columns/attributes
    sql_create_album_table = """CREATE TABLE IF NOT EXISTS album (
                                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                    type TEXT NOT NULL,
                                    title TEXT NOT NULL,
                                    artist TEXT NOT NULL,
                                    label TEXT NOT NULL,
                                    release_date INTEGER NOT NULL,
                                    asin TEXT NOT NULL,
                                    total_quantity INTEGER NOT NULL,
                                    quantity_available INTEGER NOT NULL
                                );"""

    # initialized variable with query that creates client table with columns/attributes
    sql_create_client_table = """CREATE TABLE IF NOT EXISTS client (
                                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                    firstName TEXT NOT NULL,
                                    lastName TEXT NOT NULL,
                                    physicalAddress TEXT NOT NULL,
                                    email TEXT NOT NULL,
                                    phoneNumber TEXT NOT NULL,
                                    username TEXT NOT NULL,
                                    password TEXT NOT NULL,
                                    isAdmin INTEGER NOT NULL,
                                    isLogged INTEGER NOT NULL,
                                    lastLogged INTEGER NOT NULL
                                );"""

    # initialized variable with query that creates book_copy table with columns/attributes
    #FOREIGN KEY(book_id) REFERENCES book(id),
    sql_create_book_copy_table = """CREATE TABLE IF NOT EXISTS book_copy (
                                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                    book_id INTEGER NOT NULL,
                                    isLoaned INTEGER NOT NULL,
                                    FOREIGN KEY(book_id) REFERENCES book(id)
                                );"""

    # initialized variable with query that creates magazine_copy table with columns/attributes
    sql_create_magazine_copy_table = """CREATE TABLE IF NOT EXISTS magazine_copy (
                                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                    magazine_id INTEGER NOT NULL,
                                    isLoaned INTEGER NOT NULL,
                                    FOREIGN KEY(magazine_id) REFERENCES magazine(id)
                                );"""

    # initialized variable with query that creates movie_copy table with columns/attributes
    sql_create_movie_copy_table = """CREATE TABLE IF NOT EXISTS movie_copy (
                                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                    movie_id INTEGER NOT NULL,
                                    isLoaned INTEGER NOT NULL,
                                    FOREIGN KEY(movie_id) REFERENCES movie(id)
                                );"""

    # initialized variable with query that creates album_copy table with columns/attributes
    sql_create_album_copy_table = """CREATE TABLE IF NOT EXISTS album_copy (
                                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                    album_id INTEGER NOT NULL,
                                    isLoaned INTEGER NOT NULL,
                                    FOREIGN KEY(album_id) REFERENCES album(id)
                                );"""

    if database.connection is None:
        print("Error! cannot create the database connection.")
        return

    # creates book table inside database
    create_table(database, sql_create_book_table)
    # create magazine table inside database
    create_table(database, sql_create_magazine_table)
    # create movie table inside database
    create_table(database, sql_create_movie_table)
    # create album table inside database
    create_table(database, sql_create_album_table)
    # create client table inside database
    create_table(database, sql_create_client_table)
    # create book copy table inside database
    create_table(database, sql_create_book_copy_table)
    # create magazine copy table inside database
    create_table(database, sql_create_magazine_copy_table)
    # create movie copy table inside database
    create_table(database, sql_create_movie_copy_table)
    # create album copy table inside database
    create_table(database, sql_create_album_copy_table)

    COPIES = 3
    NUM_BOOKS = 50
    MAX_BOOK_PAGES = 1500
    NUM_MAGAZINES = 50
    NUM_MOVIES = 50
    NUM_ALBUMS = 50
    NUM_USERS = 50
    book_types = ['Paperback', 'Hardcover', 'Graphic', 'Coffee Table Book', 'Textbook']
    languages = ['English', 'French', 'Italian', 'Spanish', 'Greek', 'Russian', 'German']
    album_types = ["Vinyl", "CD", "Cassette"]
    MAX_QUANTITY = 10
    MAX_TOTAL = 4

    catalog_controll = catalog_controller.get_instance()
    admin_controll = admin_controller.get_instance()
    client_controll = client_controller.get_instance()

    movie_name = lambda: "The " + f.job() if f.random_int() % 2 == 0 else " ".join(f.words()).capitalize()
    album_name = movie_name
    names = lambda: ", ".join([f.name() for x in range(1 + f.random_int() % 9)])
    date = lambda: int(time.time() - f.random_int() * f.random_int())
    asin = lambda: "".join(
        [f.random_letter().upper() if f.random_int() % 2 == 0 else str(f.random_digit()) for x in range(10)])
    phone_number = lambda: "".join([str(f.random_digit()) for x in range(3)]) + "-" + "".join(
        [str(f.random_digit()) for x in range(3)]) + "-" + "".join([str(f.random_digit()) for x in range(4)])

    # Fake data generator
    f = Faker()

    for b in range(NUM_BOOKS):
        book_attributes = {'author': f.name(),
                           'title': f.catch_phrase(),
                           'format': book_types[f.random_int() % len(book_types)],
                           'pages': f.random_int() % MAX_BOOK_PAGES,
                           'publisher': f.last_name(),
                           'year_of_publication': (f.random_int() % 100) + 1910,
                           'language': languages[f.random_int()% len(languages)],
                           'isbn_10': f.isbn10(),
                           'isbn_13': f.isbn13(),
                           'total_quantity': 3,
                           'quantity_available': 3
                           }
        book_copy = (b+1, 0)
        new_book = Book(book_attributes)
        catalog_controll.view_catalog_inventory()[catalog_controll.BOOK_TYPE].add(new_book, True)
        # Create copies of the same book - also done for every record type below
        for cop in range(COPIES):
            create_book_copy(database, book_copy)

    for m in range(NUM_MAGAZINES):
        magazine_attributes = {'title': f.word().upper(),
                               'publisher': f.last_name(),
                               'year_of_publication': f.random_int() % 100 + 1910,
                               'language': languages[f.random_int() % len(languages)],
                               'isbn_10': f.isbn10(),
                               'isbn_13': f.isbn13(),
                               'total_quantity': 3,
                               'quantity_available': 3
                               }
        magazine_copy = (m+1, 0)
        new_magazine = Magazine(magazine_attributes)
        catalog_controll.view_catalog_inventory()[catalog_controll.MAGAZINE_TYPE].add(new_magazine, True)

        for cop in range(COPIES):
            create_magazine_copy(database, magazine_copy)

    for m in range(NUM_MOVIES):
        movie_attributes = {'title':movie_name(),
                            'director': f.name(),
                            'producers': names(),
                            'actors': names(),
                            'language': languages[f.random_int() % len(languages)],
                            'subtitles': languages[f.random_int() % len(languages)],
                            'dubbed': languages[f.random_int() % len(languages)],
                            'release_date': date(),
                            'run_time': 60 + f.random_int() % (2 * 60),
                            'total_quantity': 3,
                            'quantity_available': 3
                            }
        movie_copy = (m+1, 0)
        new_movie = Movie(movie_attributes)
        catalog_controll.view_catalog_inventory()[catalog_controll.MOVIE_TYPE].add(new_movie, True)
        for cop in range(COPIES):
            create_movie_copy(database, movie_copy)

    for a in range(NUM_ALBUMS):
        album_attributes = {'type': album_types[f.random_int() % len(album_types)],
                            'title': album_name(),
                            'artist': f.name(),
                            'label': f.word().upper(),
                            'release_date': date(),
                            'asin': asin(),'total_quantity': 3,
                            'quantity_available': 3
                            }
        album_copy = (a+1, 0)
        new_album = Album(album_attributes)
        catalog_controll.view_catalog_inventory()[catalog_controll.ALBUM_TYPE].add(new_album, True)
        for cop in range(COPIES):
            create_album_copy(database, album_copy)

    for u in range(NUM_USERS):
        user_attributes = {'firstName': f.first_name(),
                             'lastName': f.last_name(),
                             'physicalAddress': f.address().replace("\n", ", "),
                             'email': f.email(),
                             'phoneNumber': phone_number(),
                             'username': f.user_name(),
                             'password': f.password(),
                             'isAdmin': f.random_int() % 2,
                             'isLogged': f.random_int() % 2,
                             'lastLogged': int(time.time() - f.random_int() * f.random_int())
                             }
        new_user = User(user_attributes)
        if new_user._is_admin == 1:
            admin_controll._admin_catalog.add(new_user,True)
        elif new_user._is_admin ==0:
            client_controll._client_catalog.add(new_user, True)

    client1 = dict((('firstName', "Aaron"), ('lastName','Doe'), ('physicalAddress','1451 De Maisonneuve Blvd. W. Montreal, QC H3G 1M8 Canada'),
                    ('email','student1@hotmail.com'), ('phoneNumber','514-555-0001'), ( 'username' ,'antman'), ('password','password1'), ('isAdmin',0), ('isLogged',1), ('lastLogged',1537207100)))

    client2 = dict((('firstName', "Chloe"), ('lastName', 'Doe'),
          ('physicalAddress', '1452 De Maisonneuve Blvd. W. Montreal, QC H3G 1M8 Canada'),
          ('email', 'student2@hotmail.com'), ('phoneNumber', '514-555-0002'), ('username', 'catwoman'),
          ('password', 'password3'), ('isAdmin', 1), ('isLogged', 1), ('lastLogged', 1537207100)))

    new_client1 = User(client1)
    new_client2 = User(client2)
    # create a new clients inside client table
    client_controll._client_catalog.add(new_client1, True)
    admin_controll._admin_catalog.add(new_client2, True)

    #close database connection
    database.close_connection()


# run main function
if __name__ == '__main__':
    main()
