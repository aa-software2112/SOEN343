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
        return redirect('/adminView/adminViewCatalog')