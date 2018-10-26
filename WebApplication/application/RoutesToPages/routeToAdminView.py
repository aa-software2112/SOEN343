from flask import render_template, g, session, redirect, request,flash
from application import app
from application import userController, adminController
from application import databaseObject as db
from application.Classes.Book import Book
from application.Classes.Magazine import Magazine
from application.Classes.Album import Album
from application.Classes.Movie import Movie
from application.CommonDefinitions.HelperFunctions import login_required, admin_required
import random

@app.route('/adminView')
@login_required
@admin_required
def adminView():
	return render_template('administratorView.html')
	
@app.route('/adminView/userCreator')
@login_required
@admin_required
def userCreator():
	return render_template('userCreator.html')
	
@app.route('/adminView/adminViewUserRegistry')
@login_required
@admin_required
def adminViewUserRegistry():

	return render_template('administratorViewUserRegistry.html', allLoggedClients = adminController.getAllLoggedClient())
	
@app.route('/adminView/adminViewCatalog', methods=['GET','POST'])
@login_required
@admin_required
def adminViewCatalog():

        dict_of_catalogs = adminController.view_inventory()
        # comment this out when fully implemented
        #for catalog_name in dict_of_catalogs.keys():
         #   print("*****\nDictionary: {}\n*****".format(catalog_name))
          #  dict_of_objects = dict_of_catalogs[catalog_name]
           # for object_id, media_object in dict_of_objects.items():
            #    print ("ID {} OBJ {}".format(object_id, media_object))

        return render_template('administratorViewCatalog.html', dict_of_catalogs=dict_of_catalogs)

@app.route('/registerUser', methods=['POST'])
@login_required
@admin_required
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
@login_required
@admin_required
def adminViewAddToCatalog():

	return render_template('administratorViewAddToCatalog.html')

@app.route('/adminView/adminViewAddBook', methods=['POST', 'GET'])
@login_required
@admin_required
def adminViewAddBook():
    if request.method == 'POST':

        adminController.add_new_book(request.form)
        flash("Book Entry Created Successfully!!", 'success')
        return redirect('/adminView/adminViewCatalog')
    return render_template('addBook.html')

@app.route('/adminView/adminViewAddMovie', methods=['POST', 'GET'])
@login_required
@admin_required
def adminViewAddMovie():
    if request.method == 'POST':

        adminController.add_new_movie(request.form)
        flash("Movie Entry Created Successfully!!", 'success')
        return redirect('/adminView/adminViewCatalog')
    return render_template('addMovie.html')

@app.route('/adminView/adminViewAddMagazine', methods=['POST', 'GET'])
@login_required
@admin_required
def adminViewAddMagazine():
        if request.method == 'POST':

            adminController.add_new_magazine(request.form)
            flash("Magazine Entry Created Successfully!!", 'success')
            return redirect('/adminView/adminViewCatalog')
        return render_template('addMagazine.html')

@app.route('/adminView/adminViewAddAlbum', methods=['POST', 'GET'])
@login_required
@admin_required
def adminViewAddAlbum():
    if request.method == 'POST':

        adminController.add_new_album(request.form)
        flash("Album Entry Created Successfully!!", 'success')
        return redirect('/adminView/adminViewCatalog')
    return render_template('AddAlbum.html')

@app.route('/adminView/modifyBookForm', methods=['GET', 'POST'])
@login_required
@admin_required
def modify_book_form():

    id=request.form['modify_book']
    #print(adminController.get_book_by_id(int(id)))
    return render_template('modifyBook.html', book=adminController.get_book_by_id(int(id)))

@app.route('/modifyBook', methods=['POST'])
@login_required
@admin_required
def modify_book():

    adminController.modify_book(request.form)
    flash("Book modified succesfully.", 'success')
    return redirect('/adminView/adminViewCatalog')

@app.route('/adminView/modifyMagazineForm', methods=['GET', 'POST'])
@login_required
@admin_required
def modify_magazine_form():

    id = request.form['modify_magazine']
    return render_template('modifyMagazine.html', magazine=adminController.get_magazine_by_id(int(id)))

@app.route('/modifyMagazine', methods=['POST'])
@login_required
@admin_required
def modify_magazine():

    adminController.modify_magazine(request.form)
    flash("Magazine modified succesfully.", 'success')
    return redirect('/adminView/adminViewCatalog')

@app.route('/adminView/modifyAlbumForm', methods=['GET', 'POST'])
@login_required
@admin_required
def modify_album_form():
    id = request.form['modify_album']
    return render_template('modifyAlbum.html', album=adminController.get_album_by_id(int(id)))

@app.route('/modifyAlbum', methods=['POST'])
@login_required
@admin_required
def modify_album():

    adminController.modify_album(request.form)
    flash("Album modified succesfully.", 'success')
    return redirect('/adminView/adminViewCatalog')

@app.route('/adminView/modifyMovieForm', methods=['GET', 'POST'])
@login_required
@admin_required
def modify_movie_form():

    id=request.form['modify_movie']
    return render_template('modifyMovie.html', movie=adminController.get_movie_by_id(int(id)))

@app.route('/modifyMovie', methods=['POST'])
@login_required
@admin_required
def modify_movie():

    adminController.modify_movie(request.form)
    flash("Movie modified succesfully.", 'success')
    return redirect('/adminView/adminViewCatalog')

@app.route('/deleteCatalog', methods=['POST'])
@login_required
@admin_required
def deleteCatalog():

    id = request.form["id"]
    type = request.form["type"]
    adminController.delete_catalog(int(id), type)

    flash("Entry deleted succesfully.", 'success')
    return redirect('/adminView/adminViewCatalog')