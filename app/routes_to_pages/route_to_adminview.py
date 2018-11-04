from flask import render_template, g, session, redirect, request, flash
from app import app
from app import clientController, adminController
from app.controllers.catalog_controller import CatalogController
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

    return render_template('admin_view_user_registry.html', allLoggedClients=adminController.get_all_logged_admins() + clientController.get_all_logged_clients())


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

    # Cannot create a new user if it exists as either client or administrator
    emaillist = clientController.get_client_by_email(email) + adminController.get_admin_by_email(email)
    usernamelist = clientController.get_client_by_username(username) + adminController.get_admin_by_username(username)

    if (len(usernamelist) == 0) & (len(emaillist) == 0):

        # Create an administrator
        if int(typeofclient) == 1:

            adminController.create_admin(firstname, lastname, address, email, phonenumber, username, password, 0, 0)

            flash("User created successfully.", 'success')

        # Create a client
        else:

            clientController.create_client(firstname, lastname, address, email, phonenumber, username, password, 0, 0)

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
        adminController.add_entry_to_catalog(CatalogController.BOOK_TYPE, request.form)
        flash("Book entry created successfully.", 'success')
        return redirect('/adminView/adminViewCatalog')
    return render_template('add_book.html')


@app.route('/adminView/adminViewAddMovie', methods=['POST', 'GET'])
@login_required
@admin_required
def adminViewAddMovie():
    if request.method == 'POST':
        adminController.add_entry_to_catalog(CatalogController.MOVIE_TYPE, request.form)
        flash("Movie entry created successfully.", 'success')
        return redirect('/adminView/adminViewCatalog')
    return render_template('add_movie.html')


@app.route('/adminView/adminViewAddMagazine', methods=['POST', 'GET'])
@login_required
@admin_required
def adminViewAddMagazine():
    if request.method == 'POST':
        adminController.add_entry_to_catalog(CatalogController.MAGAZINE_TYPE, request.form)
        flash("Magazine entry created successfully.", 'success')
        return redirect('/adminView/adminViewCatalog')
    return render_template('add_magazine.html')


@app.route('/adminView/adminViewAddAlbum', methods=['POST', 'GET'])
@login_required
@admin_required
def adminViewAddAlbum():
    if request.method == 'POST':
        adminController.add_entry_to_catalog(CatalogController.ALBUM_TYPE, request.form)
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
        return render_template('modify_book.html', book=adminController.get_catalog_entry_by_id(CatalogController.BOOK_TYPE, int(id)))
    if (type == 2):
        return render_template('modify_movie.html', movie=adminController.get_catalog_entry_by_id(CatalogController.MOVIE_TYPE, int(id)))
    if (type == 3):
        return render_template('modify_magazine.html', magazine=adminController.get_catalog_entry_by_id(CatalogController.MAGAZINE_TYPE, int(id)))
    if (type == 4):
        return render_template('modify_album.html', album=adminController.get_catalog_entry_by_id(CatalogController.ALBUM_TYPE, int(id)))


@app.route('/modifyCatalog', methods=['POST'])
@login_required
@admin_required
def modify_catalog():
    type = request.form["type"]
    adminController.modify_catalog(type, request.form)
    flash("Entry modified succesfully.", 'success')
    return redirect('/adminView/adminViewCatalog')

@app.route('/adminView/deleteViewRecords', methods=['GET', 'POST'])
def delete_view_catalog():
   
    type = int(request.form["type"])
    id = request.form["id"]

    if (type == 1):
        catalog_type = CatalogController.BOOK_TYPE
    elif (type == 2):
        catalog_type = CatalogController.MOVIE_TYPE
    elif (type == 3):
        catalog_type = CatalogController.MAGAZINE_TYPE
    elif (type == 4):
        catalog_type = CatalogController.ALBUM_TYPE
        
    catalog_record = adminController.get_catalog_entry_by_id(catalog_type, int(id))
    catalog_record_copy = adminController.get_catalog_copies_by_id(catalog_type, int(id))

    return render_template('delete_record_modal.html', catalog_type = int(catalog_type), catalog_record = catalog_record, catalog_record_copy = catalog_record_copy)

@app.route('/deleteCatalog', methods=['POST'])
@login_required
@admin_required
def delete_catalog():

    id = request.form["id"]
    catalog_type = request.form["type"]
    print("Backend ID: " + id)
    adminController.delete_catalog_copy_entry(catalog_type, int(id))

    flash("Entry deleted succesfully.", 'success')
    return redirect('/adminView/adminViewCatalog')
