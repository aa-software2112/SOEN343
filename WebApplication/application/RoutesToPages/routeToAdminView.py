from flask import render_template, g, session, redirect, request,flash
from application import app
from application import userController, adminController
from application import databaseObject as db
from application.Classes.Book import Book
from application.Classes.Magazine import Magazine
from application.Classes.Album import Album
from application.Classes.Movie import Movie
import random

@app.route('/adminView')
def adminView():

	if g.user["isAdmin"]:
		return render_template('administratorView.html')
	return redirect('/index')
	
@app.route('/adminView/userCreator')
def userCreator():

	return render_template('userCreator.html')
	
@app.route('/adminView/adminViewUserRegistry')
def adminViewUserRegistry():

	return render_template('administratorViewUserRegistry.html', allLoggedClients = adminController.getAllLoggedClient())
	
@app.route('/adminView/adminViewCatalog', methods=['GET','POST'])
def adminViewCatalog():

        dict_of_catalogs = adminController.view_inventory()
        # comment this out when fully implemented
        for catalog_name in dict_of_catalogs.keys():
            print("*****\nDictionary: {}\n*****".format(catalog_name))
            dict_of_objects = dict_of_catalogs[catalog_name]
            for object_id, media_object in dict_of_objects.items():
                print ("ID {} OBJ {}".format(object_id, media_object))

        return render_template('administratorViewCatalog.html', dict_of_catalogs=dict_of_catalogs)

@app.route('/registerUser', methods=['POST'])
def registerUser():
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    phonenumber = request.form["phonenumber"]
    email = request.form["email"]
    username = request.form["username"]
    password = request.form["password"]
    address = request.form["address"]
    typeofclient = request.form["isadmin"]


    emaillist = userController.getClientByEmail(email)
    usernamelist = userController.getClientByUsername(username)

    if (len(usernamelist) == 0) & (len(emaillist) == 0):

        userController.createClient(firstname, lastname, address, email, phonenumber, username, password, typeofclient, 0, 0)
        flash("User Created Successfully!!",'success')

        return redirect("/")
    else:
        error = "Username or email already exist !"
        return render_template('UserCreator.html',  error=error)

@app.route('/adminView/adminViewAddToCatalog')
def adminViewAddToCatalog():

	return render_template('administratorViewAddToCatalog.html')


@app.route('/adminView/adminViewAddBook', methods=['POST', 'GET'])
def adminViewAddBook():
    if request.method == 'POST':
        _author = request.form.get('author')
        _title = request.form.get('title')
        _format = request.form.get('format')
        _pages = request.form.get('pages')
        _publisher = request.form.get('publisher')
        _year_of_publication = request.form.get('year_of_publication')
        _language = request.form.get('language')
        _isbn_10 = request.form.get('isbn_10')
        _isbn_13 = request.form.get('isbn_13')

        book_attributes = {
            'id': 0,
            'author': _author,
            'title': _title,
            'format': _format,
            'pages': _pages,
            'publisher': _publisher,
            'year_of_publication': _year_of_publication,
            'language': _language,
            'isbn_10': _isbn_10,
            'isbn_13': _isbn_13
        }
        new_book = Book(book_attributes)
        adminController.add_new_book(new_book)
        flash("Book Entry Created Successfully!!", 'success')
        return redirect('/adminView/adminViewCatalog')
    return render_template('addBook.html')


@app.route('/adminView/adminViewAddMovie', methods=['POST', 'GET'])
def adminViewAddMovie():
    if request.method == 'POST':
        _title = request.form.get('title')
        _director = request.form.get('director')
        _producers = request.form.get('producers')
        _actors = request.form.get('actors')
        _language = request.form.get('language')
        _subtitles = request.form.get('subtitles')
        _dubbed = request.form.get('dubbed')
        _release_date = request.form.get('release_date')
        _run_time = request.form.get('run_time')

        movie_attributes = {
            'id': 0,
            'title': _title,
            'director': _director,
            'producers': _producers,
            'actors': _actors,
            'language': _language,
            'subtitles': _subtitles,
            'dubbed': _dubbed,
            'release_date': _release_date,
            'run_time': _run_time
        }
        new_movie = Movie(movie_attributes)
        adminController.add_new_movie(new_movie)
        flash("Movie Entry Created Successfully!!", 'success')
        return redirect('/adminView/adminViewCatalog')
    return render_template('addMovie.html')

@app.route('/adminView/adminViewAddMagazine', methods=['POST', 'GET'])
def adminViewAddMagazine():
        if request.method == 'POST':
            _title = request.form.get('title')
            _publisher = request.form.get('publisher')
            _year_of_publication = request.form.get('year_of_publication')
            _language = request.form.get('language')
            _isbn_10 = request.form.get('isbn_10')
            _isbn_13 = request.form.get('isbn_13')

            magazine_attributes = {
                'id': 0,
                'title': _title,
                'publisher': _publisher,
                'year_of_publication': _year_of_publication,
                'language': _language,
                'isbn_10': _isbn_10,
                'isbn_13': _isbn_13
            }

            new_magazine = Magazine(magazine_attributes)
            adminController.add_new_magazine(new_magazine)
            flash("Magazine Entry Created Successfully!!", 'success')
            return redirect('/adminView/adminViewCatalog')
        return render_template('addMagazine.html')

@app.route('/adminView/adminViewAddAlbum', methods=['POST', 'GET'])
def adminViewAddAlbum():
    if request.method == 'POST':
        _type = request.form.get('type')
        _title = request.form.get('title')
        _artist = request.form.get('artist')
        _label = request.form.get('label')
        _release_date = request.form.get('release_date')
        _asin = request.form.get('asin')

        album_attributes = {
            'id': 0,
            'type': _type,
            'title': _title,
            'artist': _artist,
            'label': _label,
            'release_date': _release_date,
            'asin': _asin,
        }
        new_album=Album(album_attributes)
        adminController.add_new_album(new_album)
        flash("Album Entry Created Successfully!!", 'success')
        return redirect('/adminView/adminViewCatalog')

    return render_template('AddAlbum.html')

@app.route('/adminView/modifyBookForm', methods=['GET', 'POST'])
def modify_book_form():
    id=request.form['modify_book']
    #print(adminController.get_book_by_id(int(id)))
    return render_template('modifyBook.html', book=adminController.get_book_by_id(int(id)))

@app.route('/modifyBook', methods=['POST'])
def modify_book():
        id = request.form["id"]
        author = request.form["author"]
        title = request.form["title"]
        format = request.form["format"]
        pages = request.form["pages"]
        publisher = request.form["publisher"]
        year_of_publication = request.form["year_of_publication"]
        language = request.form["language"]
        isbn_10 = request.form["isbn_10"]
        isbn_13 = request.form["isbn_13"]

        attributes = {'id': int(id),
                      'author': author,
                      'title': title,
                      'format': format,
                      'pages': pages,
                      'publisher': publisher,
                      'year_of_publication': year_of_publication,
                      'language': language,
                      'isbn_10': isbn_10,
                      'isbn_13': isbn_13
                      }
        
        modified_book = Book(attributes)
        adminController.modify_book(modified_book)
        flash("Book modified succesfully.", 'success')
        return redirect('/adminView/adminViewCatalog')

@app.route('/adminView/modifyMagazineForm', methods=['GET', 'POST'])
def modify_magazine_form():
    id = request.form['modify_magazine']
    return render_template('modifyMagazine.html', magazine=adminController.get_magazine_by_id(int(id)))

@app.route('/modifyMagazine', methods=['POST'])
def modify_magazine():
        id = request.form["id"]
        title = request.form["title"]
        publisher = request.form["publisher"]
        year_of_publication = request.form["year_of_publication"]
        language = request.form["language"]
        isbn_10 = request.form["isbn_10"]
        isbn_13 = request.form["isbn_13"]

        attributes = {'id': int(id),
                      'title': title,
                      'publisher': publisher,
                      'year_of_publication': year_of_publication,
                      'language': language,
                      'isbn_10': isbn_10,
                      'isbn_13': isbn_13
                      }

        modified_magazine = Magazine(attributes)
        adminController.modify_magazine(modified_magazine)
        flash("Magazine modified succesfully.", 'success')
        return redirect('/adminView/adminViewCatalog')

@app.route('/adminView/modifyAlbumForm', methods=['GET', 'POST'])
def modify_album_form():
    id = request.form['modify_album']
    return render_template('modifyAlbum.html', album=adminController.get_album_by_id(int(id)))

@app.route('/modifyAlbum', methods=['POST'])
def modify_album():
        id = request.form["id"]
        type = request.form["type"]
        title = request.form["title"]
        artist = request.form["artist"]
        label = request.form["label"]
        release_date = request.form["release_date"]
        asin = request.form["asin"]

        attributes = {'id': int(id),
                      'type': type,
                      'title': title,
                      'artist': artist,
                      'label': label,
                      'release_date': release_date,
                      'asin': asin
                      }

        modified_album = Album(attributes)
        adminController.modify_album(modified_album)
        flash("Album modified succesfully.", 'success')
        return redirect('/adminView/adminViewCatalog')

@app.route('/adminView/modifyMovieForm', methods=['GET', 'POST'])
def modify_movie_form():
    id=request.form['modify_movie']
    return render_template('modifyMovie.html', movie=adminController.get_movie_by_id(int(id)))

@app.route('/modifyMovie', methods=['POST'])
def modify_movie():
        id = request.form["id"]
        title = request.form["title"]
        director = request.form["director"]
        producers = request.form["producers"]
        actors = request.form["actors"]
        language = request.form["language"]
        subtitles = request.form["subtitles"]
        dubbed = request.form["dubbed"]
        release_date = request.form["release_date"]
        run_time = request.form["run_time"]

        attributes = {'id': int(id),
                      'title': title,
                      'director': director,
                      'producers': producers,
                      'actors': actors,
                      'language': language,
                      'subtitles': subtitles,
                      'language': language,
                      'dubbed': dubbed,
                      'release_date': release_date,
                      'run_time': run_time
                      }

        modified_movie = Movie(attributes)
        adminController.modify_movie(modified_movie)
        flash("Movie modified succesfully.", 'success')
        return redirect('/adminView/adminViewCatalog')


@app.route('/deleteCatalog', methods=['POST'])
def deleteCatalog():

  id = request.form["id"]
  type = request.form["type"]

  adminController.delete_catalog(int(id), type)

  flash("Entry deleted succesfully.", 'success')
  return redirect('/adminView/adminViewCatalog')