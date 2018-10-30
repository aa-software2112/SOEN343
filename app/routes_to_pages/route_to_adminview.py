from flask import render_template, g, session, redirect, request, flash
from app import app
from app import userController, adminController
from app import databaseObject as db
from app.classes.book import Book
from app.classes.magazine import Magazine
from app.classes.album import Album
from app.classes.movie import Movie
from app.common_definitions.helper_functions import login_required, admin_required
import random


@app.route('/adminView')
@login_required
@admin_required
def adminView():
    return render_template('admin_view.html')


@app.route('/adminView/userCreator')
@login_required
@admin_required
def userCreator():
    return render_template('user_creator.html')


@app.route('/adminView/adminViewUserRegistry')
@login_required
@admin_required
def adminViewUserRegistry():

    return render_template('admin_view_user_registry.html', allLoggedClients=adminController.get_all_logged_client())


@app.route('/adminView/adminViewCatalog', methods=['GET', 'POST'])
@login_required
@admin_required
def adminViewCatalog():

    dict_of_catalogs = adminController.view_inventory()
    # comment this out when fully implemented
    # for catalog_name in dict_of_catalogs.keys():
    #   print("*****\nDictionary: {}\n*****".format(catalog_name))
    #  dict_of_objects = dict_of_catalogs[catalog_name]
    # for object_id, media_object in dict_of_objects.items():
    #    print ("ID {} OBJ {}".format(object_id, media_object))

    return render_template('admin_view_catalog.html', dict_of_catalogs=dict_of_catalogs)


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

    emaillist = userController.get_client_by_email(email)
    usernamelist = userController.get_client_by_username(username)

    if (len(usernamelist) == 0) & (len(emaillist) == 0):

        userController.create_client(
            firstname, lastname, address, email, phonenumber, username, password, typeofclient, 0, 0)
        flash("User created successfully.", 'success')

        return redirect("/")
    else:
        error = "Username or email already exist !"
        return render_template('user_creator.html',  error=error)


@app.route('/adminView/adminViewAddToCatalog')
@login_required
@admin_required
def adminViewAddToCatalog():

    return render_template('admin_view_add_to_catalog.html')


@app.route('/adminView/adminViewAddBook', methods=['POST', 'GET'])
@login_required
@admin_required
def adminViewAddBook():
    if request.method == 'POST':
        type = int(request.form["type"])
        adminController.add_new_catalog(type, request.form)
        flash("Book entry created successfully.", 'success')
        return redirect('/adminView/adminViewCatalog')
    return render_template('add_book.html')


@app.route('/adminView/adminViewAddMovie', methods=['POST', 'GET'])
@login_required
@admin_required
def adminViewAddMovie():
    if request.method == 'POST':
        type = int(request.form["type"])
        adminController.add_new_catalog(type, request.form)
        flash("Movie entry created successfully.", 'success')
        return redirect('/adminView/adminViewCatalog')
    return render_template('add_movie.html')


@app.route('/adminView/adminViewAddMagazine', methods=['POST', 'GET'])
@login_required
@admin_required
def adminViewAddMagazine():
    if request.method == 'POST':
        type = int(request.form["type"])
        adminController.add_new_catalog(type, request.form)
        flash("Magazine entry created successfully.", 'success')
        return redirect('/adminView/adminViewCatalog')
    return render_template('add_magazine.html')


@app.route('/adminView/adminViewAddAlbum', methods=['POST', 'GET'])
@login_required
@admin_required
def adminViewAddAlbum():
    if request.method == 'POST':
        type = int(request.form["type"])
        adminController.add_new_catalog(type, request.form)
        flash("Album entry created successfully.", 'success')
        return redirect('/adminView/adminViewCatalog')
    return render_template('add_album.html')


@app.route('/adminView/modifyCatalogForm', methods=['GET', 'POST'])
@login_required
@admin_required
def modify_catalog_form():
    type = int(request.form["type"])
    id = request.form['modify_catalog']
    if (type == 1):
        return render_template('modify_book.html', book=adminController.get_book_by_id(int(id)))
    if (type == 2):
        return render_template('modify_movie.html', movie=adminController.get_movie_by_id(int(id)))
    if (type == 3):
        return render_template('modify_magazine.html', magazine=adminController.get_magazine_by_id(int(id)))
    if (type == 4):
        return render_template('modify_album.html', album=adminController.get_album_by_id(int(id)))


@app.route('/modifyCatalog', methods=['POST'])
@login_required
@admin_required
def modify_catalog():
    type = int(request.form["type"])
    adminController.modify_catalog(type, request.form)
    flash("Entry modified succesfully.", 'success')
    return redirect('/adminView/adminViewCatalog')


@app.route('/deleteCatalog', methods=['POST'])
@login_required
@admin_required
def delete_catalog():

    id = request.form["id"]
    type = request.form["type"]
    adminController.delete_catalog(int(id), type)

    flash("Entry deleted succesfully.", 'success')
    return redirect('/adminView/adminViewCatalog')
