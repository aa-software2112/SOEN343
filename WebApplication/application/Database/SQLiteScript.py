import sqlite3
from sqlite3 import Error
import glob

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
    sql = ''' INSERT INTO book(title,author,format,pages,publisher,language,isbn_10,isbn_13,isLoaned)
              VALUES(?,?,?,?,?,?,?,?,?) '''
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
   
    sql = ''' INSERT INTO movie(title,director,producers,actors,language,subtitles,dubbed,releaseDate,runTime,isLoaned)
              VALUES(?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, movie)

#function takes database connection object 'conn' and a music 
#creates a new music into the music table
def create_music(conn, music):
    sql = ''' INSERT INTO music(type,title,artist,label,releaseDate,asin,isLoaned)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, music)

#function takes database connection object 'conn' and a client 
#creates a new client into the client table
def create_client(conn, client):
    sql = ''' INSERT INTO client(firstName,lastName,physicalAddress,email,phoneNumber,username,password,isAdmin,isLogged,lastLogged)
              VALUES(?,?,?,?,?,?,?,?,?,?) '''
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
def initializeAndFillDatabase(pathToDB):
    
	# Database already exists; do nothing
	if len(glob.glob(pathToDB)) == 1:
		return

	conn = create_connection(pathToDB)

	#initialized variable with query that creates book table with columns/attributes
	sql_create_book_table = """CREATE TABLE IF NOT EXISTS book (
									id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
									author TEXT NOT NULL,
									title TEXT NOT NULL,
									format TEXT NOT NULL,
									pages INTEGER NOT NULL,
									publisher TEXT NOT NULL,
									year_of_publication TEXT NOT NULL,
									language TEXT NOT NULL,
									isbn_10 TEXT NOT NULL,
									isbn_13 TEXT NOT NULL
								);"""

	#initialized variable with query that creates magazine table with columns/attributes
	sql_create_magazine_table = """CREATE TABLE IF NOT EXISTS magazine (
									id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
									title TEXT NOT NULL,
									publisher TEXT NOT NULL,
									year_of_publication TEXT NOT NULL,
									language TEXT NOT NULL,
									isbn_10 TEXT NOT NULL,
									isbn_13 TEXT NOT NULL
								);"""

	#initialized variable with query that creates movie table with columns/attributes
	sql_create_movie_table = """CREATE TABLE IF NOT EXISTS movie (
									id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
									title TEXT NOT NULL,
									director TEXT NOT NULL,
									producers TEXT NOT NULL,
									actors TEXT NOT NULL,
									language TEXT NOT NULL,
									subtitles TEXT NOT NULL,
									dubbed TEXT NOT NULL,
									releaseDate TEXT NOT NULL,
									runTime INTEGER NOT NULL
								);"""

	#initialized variable with query that creates album table with columns/attributes
	sql_create_album_table = """CREATE TABLE IF NOT EXISTS album (
									id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
									type TEXT NOT NULL,
									title TEXT NOT NULL,
									artist TEXT NOT NULL,
									label TEXT NOT NULL,
									releaseDate TEXT NOT NULL,
									asin TEXT NOT NULL
								);"""

	#initialized variable with query that creates client table with columns/attributes
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
		
	if conn is not None:
		#creates book table inside database
		create_table(conn, sql_create_book_table)
		#create magazine table inside database
		create_table(conn, sql_create_magazine_table)
		#create movie table inside database
		create_table(conn, sql_create_movie_table)
		#create music table inside database
		create_table(conn, sql_create_album_table)
		#create client table inside database
		create_table(conn, sql_create_client_table)
	else:
		print("Error! cannot create the database connection.")

	with conn:
		#create a new book inside book table
		book = ('Do Androids Dream of Electric Sheep?', 'Philip K. Dick', 'Paperback', 240, 'Del Rey; Reprint edition (Sept. 26 2017)', 'English', '1524796972', '978-1524796976', 1)
		create_book(conn, book)

		#create a new magazine inside magazine table
		magazine = ('TIME', 'Time (May 13 2008)', 'English', '1603200185', '978-1603200189')
		create_magazine(conn, magazine)

		#create a new movie inside movie table
		movie = ('Until the End of the World', 'Wim Wenders','Anatole Dauman, Ingrid Windisch, Joachim von Mengershausen, Pascale Daum.','Bruno Ganz, Solveig Dommartin, Otto Sander,Curt Bois, Peter Falk.','German','English','English, French','Oct. 20 2009', 127, 1)
		create_movie(conn, movie)

		#create a new music inside music table
		music = ('CD','Anastasis','Dead Can Dance', 'Sony Music', 'Aug. 14 2012','B008FOB124',0)
		create_music(conn, music)

		#store clients info inside variable so that we can insert them in client table
		client1 = ('Aaron','Doe', '1451 De Maisonneuve Blvd. W. Montreal, QC H3G 1M8 Canada', 'student1@hotmail.com','514-555-0001', 'antman', 'password1', 0, 1, 1537207100)
		client2 = ('Burns','Doe', '1452 De Maisonneuve Blvd. W. Montreal, QC H3G 1M8 Canada', 'student2@hotmail.com','514-555-0002', 'batman', 'password2', 0, 1, 1537207200)
		client3 = ('Chloe','Doe', '1453 De Maisonneuve Blvd. W. Montreal, QC H3G 1M8 Canada', 'student3@hotmail.com','514-555-0003', 'catwoman', 'password3', 1, 1, 1537207300)
		client4 = ('Donovan','Doe', '1454 De Maisonneuve Blvd. W. Montreal, QC H3G 1M8 Canada', 'student4@hotmail.com','514-555-0004', 'datman', 'password4', 0, 0, 1537207400)
		client5 = ('Eric','Doe', '1455 De Maisonneuve Blvd. W. Montreal, QC H3G 1M8 Canada', 'student5@hotmail.com','514-555-0005', 'eagleman', 'password5', 1, 1, 1537207500)

		#create a new clients inside client table
		create_client(conn, client1)
		create_client(conn, client2)
		create_client(conn, client3)
		create_client(conn, client4)
		create_client(conn, client5)

	#closes database
	close_connection(conn)
    
#run main function
if __name__ == '__main__':
    main()

