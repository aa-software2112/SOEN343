import sqlite3
from sqlite3 import Error
from faker import Faker
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


def create_table(conn, sql_create_x_table):
    """
    Function takes database connection object 'conb' and sql statement to create table 'sql_create_x_table'.  
    creates table inside database. 
    """
    try:
        c = conn.cursor()
        c.execute(sql_create_x_table)
    except Error as e:
        print(e)


def create_book(conn, book):
    """
    Function takes database connection object 'conn' and a book
    creates a new book into the book table
    """
    sql = ''' INSERT INTO book(author,title,format,pages,publisher,year_of_publication,language,isbn_10,isbn_13,total_quantity,quantity_available)
              VALUES(?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, book)


def create_magazine(conn, magazine):
    """
    Function takes database connection object 'conn' and a magazine
    creates a new magazine into the magazine table
    """
    sql = ''' INSERT INTO magazine(title,publisher,year_of_publication,language,isbn_10,isbn_13,total_quantity,quantity_available)
              VALUES(?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, magazine)


def create_movie(conn, movie):
    """
    Function takes database connection object 'conn' and a movie 
    creates a new movie into the movie  table
    """

    sql = ''' INSERT INTO movie(title,director,producers,actors,language,subtitles,dubbed,release_date,run_time,total_quantity,quantity_available)
              VALUES(?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, movie)


def create_album(conn, music):
    """
    Function takes database connection object 'conn' and a music 
    creates a new music into the music table
    """
    sql = ''' INSERT INTO album(type,title,artist,label,release_date,asin,total_quantity,quantity_available)
              VALUES(?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, music)


def create_client(conn, client):
    """
    Function takes database connection object 'conn' and a client 
    creates a new client into the client table
    """
    sql = ''' INSERT INTO client(firstName,lastName,physicalAddress,email,phoneNumber,username,password,isAdmin,isLogged,lastLogged)
              VALUES(?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, client)

def create_book_copy(conn, book):
    """
    Function takes database connection object 'conn' and a book copy
    creates a new book copy into the book copy table
    """
    sql = ''' INSERT INTO book_copy(book_id,isLoaned)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, book)

def create_magazine_copy(conn, magazine):
    """
    Function takes database connection object 'conn' and a magazine copy
    creates a new magazine copy into the magazine copy table
    """
    sql = ''' INSERT INTO magazine_copy(magazine_id)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, magazine)

def create_movie_copy(conn, movie):
    """
    Function takes database connection object 'conn' and a movie copy
    creates a new movie copy into the movie copy table
    """
    sql = ''' INSERT INTO movie_copy(movie_id,isLoaned)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, movie)

def create_album_copy(conn, album):
    """
    Function takes database connection object 'conn' and a album copy
    creates a new album copy into the album copy table
    """
    sql = ''' INSERT INTO album_copy(album_id,isLoaned)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, album)


def close_connection(conn):
    """
    Function takes database connection object 'conn'.
    closes connection to database (good practice)
    """
    try:
        conn.close()
    except Error as e:
        print(e)


def initializeAndFillDatabase(pathToDB):
    """
    Main where we implement most methods above (create connection, create table, insert data, close connection.)
    """

    # Database already exists; do nothing
    if len(glob.glob(pathToDB)) == 1:
        return

    conn = create_connection(pathToDB)

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

    if conn is None:
        print("Error! cannot create the database connection.")
        return

    # creates book table inside database
    create_table(conn, sql_create_book_table)
    # create magazine table inside database
    create_table(conn, sql_create_magazine_table)
    # create movie table inside database
    create_table(conn, sql_create_movie_table)
    # create album table inside database
    create_table(conn, sql_create_album_table)
    # create client table inside database
    create_table(conn, sql_create_client_table)
    # create book copy table inside database
    create_table(conn, sql_create_book_copy_table)
    # create magazine copy table inside database
    create_table(conn, sql_create_magazine_copy_table)
    # create movie copy table inside database
    create_table(conn, sql_create_movie_copy_table)
    # create album copy table inside database
    create_table(conn, sql_create_album_copy_table)

    with conn:

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
            book = (
            f.name(), f.catch_phrase(), book_types[f.random_int() % len(book_types)], f.random_int() % MAX_BOOK_PAGES,
            f.last_name(), (f.random_int() % 100) + 1910, languages[f.random_int() % len(languages)], f.isbn10(),
            f.isbn13(), 3, 3)
            book_copy = (b+1, 0)
            create_book(conn, book)
            # Create copies of the same book - also done for every record type below
            for cop in range(COPIES):
                create_book_copy(conn, book_copy)

        for m in range(NUM_MAGAZINES):
            magazine = (f.word().upper(), f.last_name(), f.random_int() % 100 + 1910,
                        languages[f.random_int() % len(languages)], f.isbn10(), f.isbn13(), 3, 3)
            magazine_copy = (m+1, 0)
            create_magazine(conn, magazine)
            for cop in range(COPIES):
                create_magazine_copy(conn, magazine_copy)

        for m in range(NUM_MOVIES):
            movie = (movie_name(), f.name(), names(), names(), languages[f.random_int() % len(languages)],
                     languages[f.random_int() % len(languages)], languages[f.random_int() % len(languages)], date(),
                     60 + f.random_int() % (2 * 60), 3, 3)
            movie_copy = (m+1, 0)
            create_movie(conn, movie)
            for cop in range(COPIES):
                create_movie_copy(conn, movie_copy)

        for a in range(NUM_ALBUMS):
            album = (
            album_types[f.random_int() % len(album_types)], album_name(), f.name(), f.word().upper(), date(), asin(), 3, 3)
            album_copy = (a+1, 0)
            create_album(conn, album)
            for cop in range(COPIES):
                create_album_copy(conn, album_copy)

        for u in range(NUM_USERS):
            client = (
            f.first_name(), f.last_name(), f.address().replace("\n", ", "), f.email(), phone_number(), f.user_name(),
            f.password(), f.random_int() % 2, f.random_int() % 2, int(time.time() - f.random_int() * f.random_int()))
            create_client(conn, client)

        client1 = ('Aaron', 'Doe', '1451 De Maisonneuve Blvd. W. Montreal, QC H3G 1M8 Canada', 'student1@hotmail.com',
                   '514-555-0001', 'antman', 'password1', 0, 1, 1537207100)
        client2 = ('Burns', 'Doe', '1452 De Maisonneuve Blvd. W. Montreal, QC H3G 1M8 Canada', 'student2@hotmail.com',
                   '514-555-0002', 'batman', 'password2', 0, 1, 1537207200)
        client3 = ('Chloe', 'Doe', '1453 De Maisonneuve Blvd. W. Montreal, QC H3G 1M8 Canada', 'student3@hotmail.com',
                   '514-555-0003', 'catwoman', 'password3', 1, 1, 1537207300)
        client4 = ('Donovan', 'Doe', '1454 De Maisonneuve Blvd. W. Montreal, QC H3G 1M8 Canada', 'student4@hotmail.com',
                   '514-555-0004', 'datman', 'password4', 0, 0, 1537207400)
        client5 = ('Eric', 'Doe', '1455 De Maisonneuve Blvd. W. Montreal, QC H3G 1M8 Canada', 'student5@hotmail.com',
                   '514-555-0005', 'eagleman', 'password5', 1, 1, 1537207500)

        # create a new clients inside client table
        create_client(conn, client1)
        create_client(conn, client2)
        create_client(conn, client3)
        create_client(conn, client4)
        create_client(conn, client5)

    # closes database
    close_connection(conn)


# run main function
if __name__ == '__main__':
    main()
