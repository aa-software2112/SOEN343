import sqlite3
from sqlite3 import Error

#function takes 'database_file_path' (exact path of database in your directory or path + name of database you wish to create. Please write it down in main method) 
#and creates database connecton to SQLite database specified inside the database_file_path. Returns connection object 'conn'
def create_connection(database_file_path):
    try:
        conn = sqlite3.connect(database_file_path)
        return conn
    except Error as e:
        print(e)
 
    return None

#function creates SQLite database in memory
#if you wish to use a temporary database, use this function but if you wish to empty previous database, simply delete the db file containing the database you wish to empty.
def create_in_memory_connection():
    try:
        conn = sqlite3.connect(':memory:')
        return conn
    except Error as e:
        print(e)
 
    return None

#function takes database connection object 'conb' and sql statement to create table 'sql_create_x_table'.  
#creates table inside database. 
def create_table(conn, sql_create_x_table):
    try:
        c = conn.cursor()
        c.execute(sql_create_x_table)
    except Error as e:
        print(e)

#function takes database connection object 'conn' and a book
#creates a new book into the book table
def create_book(conn, book):
    sql = ''' INSERT INTO book(title,author,format,pages,publisher,language,isbn_10,isbn_13)
              VALUES(?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, book)

#function takes database connection object 'conn' and a magazine
#creates a new magazine into the magazine table
def create_magazine(conn, magazine):
    sql = ''' INSERT INTO magazine(title,publisher,language,isbn_10,isbn_13)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, magazine)

#function takes database connection object 'conn' and a movie 
#creates a new movie into the movie  table
def create_movie(conn, movie):
   
    sql = ''' INSERT INTO movie(title,director,producers,actors,language,subtitles,dubbed,release_date,run_time)
              VALUES(?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, movie)

#function takes database connection object 'conn' and a music 
#creates a new music into the music table
def create_music(conn, music):
    sql = ''' INSERT INTO music(type,title,artist,label,release_date,ASIN)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, music)

#function takes database connection object 'conn' and a client 
#creates a new client into the client table
def create_client(conn, client):
    sql = ''' INSERT INTO client(id,first_name,last_name,address,email,phone,administrator)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, client)

#function takes database connection object 'conn'.
#closes connection to database (good practice)
def close_connection(conn):
    try:
        conn.close()
    except Error as e:
        print(e)

#main where we implement most methods above (create connection, create table, insert data, close connection.)
def main():
    
    #IMPORTANT: Insert your path of database below. If there's no current database, write the path + name of database you wish to create.
    database = "C:\\Users\\Anon\\Documents\\GitHub\\SOEN343\\Database\\catalog.db"

    #create a database connection
    conn = create_connection(database)
 
    #initialized variable with query that creates book table with columns/attributes
    sql_create_book_table = """CREATE TABLE IF NOT EXISTS book (
                                    title text NOT NULL,
                                    author text NOT NULL,
                                    format text NOT NULL,
                                    pages INTEGER NOT NULL,
                                    publisher text NOT NULL,
                                    language text NOT NULL,
                                    isbn_10 text NOT NULL,
                                    isbn_13 text NOT NULL,
                                    PRIMARY KEY (isbn_10, isbn_13)
                                );"""
 
    #initialized variable with query that creates magazine table with columns/attributes
    sql_create_magazine_table = """CREATE TABLE IF NOT EXISTS magazine (
                                    title text NOT NULL,
                                    publisher text NOT NULL,
                                    language text NOT NULL,
                                    isbn_10 text NOT NULL,
                                    isbn_13 text NOT NULL,
                                    PRIMARY KEY (isbn_10, isbn_13)
                                );"""
 
    #initialized variable with query that creates movie table with columns/attributes
    sql_create_movie_table = """CREATE TABLE IF NOT EXISTS movie (
                                    title text NOT NULL,
                                    director text NOT NULL,
                                    producers text NOT NULL,
                                    actors text NOT NULL,
                                    language text NOT NULL,
                                    subtitles text NOT NULL,
                                    dubbed text NOT NULL,
                                    release_date text NOT NULL,
                                    run_time text NOT NULL
                                );"""

    #initialized variable with query that creates music table with columns/attributes
    sql_create_music_table = """CREATE TABLE IF NOT EXISTS music (
                                    type text NOT NULL,
                                    title text NOT NULL,
                                    artist text NOT NULL,
                                    label text NOT NULL,
                                    release_date text NOT NULL,
                                    ASIN text NOT NULL
                                );"""

    #initialized variable with query that creates client table with columns/attributes
    sql_create_client_table = """CREATE TABLE IF NOT EXISTS client (
                                    id INTEGER PRIMARY KEY,
                                    first_name text NOT NULL,
                                    last_name text NOT NULL,
                                    address text NOT NULL,
                                    email text NOT NULL,
                                    phone text NOT NULL,
                                    administrator text NOT NULL
                                );"""
        
    if conn is not None:
        #creates book table inside database
        create_table(conn, sql_create_book_table)
        #create magazine table inside database
        create_table(conn, sql_create_magazine_table)
        #create movie table inside database
        create_table(conn, sql_create_movie_table)
        #create music table inside database
        create_table(conn, sql_create_music_table)
        #create client table inside database
        create_table(conn, sql_create_client_table)
    else:
        print("Error! cannot create the database connection.")

    with conn:
        #create a new book inside book table
        book = ('Do Androids Dream of Electric Sheep?', 'Philip K. Dick', 'Paperback', 240, 'Del Rey; Reprint edition (Sept. 26 2017)', 'English', '1524796972', '978-1524796976')
        create_book(conn, book)

        #create a new magazine inside magazine table
        magazine = ('TIME', 'Time (May 13 2008)', 'English', '1603200185', '978-1603200189')
        create_magazine(conn, magazine)

        #create a new magazine inside magazine table
        movie = ('Until the End of the World', 'Wim Wenders','Anatole Dauman, Ingrid Windisch, Joachim von Mengershausen, Pascale Daum.','Bruno Ganz, Solveig Dommartin, Otto Sander,Curt Bois, Peter Falk.','German','English','English, French','Oct. 20 2009','127 minutes')
        create_movie(conn, movie)

        #create a new magazine inside magazine table
        music = ('CD','Anastasis','Dead Can Dance', 'Sony Music', 'Aug. 14 2012','B008FOB124')
        create_music(conn, music)

        #create a new client inside client table
        client = (1,'John','Doe', '1455 De Maisonneuve Blvd. W. Montreal, QC H3G 1M8 Canada', 'student@hotmail.com', '514-555-5555', 'yes')
        create_client(conn, client)

    #closes database
    close_connection(conn)

#run main function
if __name__ == '__main__':
    main()