from flask import render_template, g, session, redirect, request, flash
from app import app
from app import client_controller, admin_controller
from app.controllers.catalog_controller import CatalogController
from app import databaseObject as db
from app.classes.book import Book
from app.classes.magazine import Magazine
from app.classes.album import Album
from app.classes.movie import Movie
from app.common_definitions.helper_functions import login_required, admin_required, convert_epoch_to_datetime
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
    list_of_clients = admin_controller.get_all_active_admins() + client_controller.get_all_active_clients()

    return render_template('admin_view_user_registry.html', list_of_clients=list_of_clients)

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
    emaillist = client_controller.get_client_by_email(email) + admin_controller.get_admin_by_email(email)
    usernamelist = client_controller.get_client_by_username(username) + admin_controller.get_admin_by_username(username)

    if (len(usernamelist) == 0) & (len(emaillist) == 0):

        # Create an administrator
        if int(typeofclient) == 1:

            admin_controller.create_admin(firstname, lastname, address, email, phonenumber, username, password, 0, 0)

            flash("User created successfully.", 'success')

        # Create a client
        else:

            client_controller.create_client(firstname, lastname, address, email, phonenumber, username, password, 0, 0)

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
        admin_controller.add_entry_to_catalog(CatalogController.BOOK_TYPE, request.form)
        flash("Book entry created successfully.", 'success')
        return redirect('viewCatalog')
    return render_template('add_book.html')


@app.route('/adminView/adminViewAddMovie', methods=['POST', 'GET'])
@login_required
@admin_required
def adminViewAddMovie():
    if request.method == 'POST':
        admin_controller.add_entry_to_catalog(CatalogController.MOVIE_TYPE, request.form)
        flash("Movie entry created successfully.", 'success')
        return redirect('viewCatalog')
    return render_template('add_movie.html')


@app.route('/adminView/adminViewAddMagazine', methods=['POST', 'GET'])
@login_required
@admin_required
def adminViewAddMagazine():
    if request.method == 'POST':
        admin_controller.add_entry_to_catalog(CatalogController.MAGAZINE_TYPE, request.form)
        flash("Magazine entry created successfully.", 'success')
        return redirect('viewCatalog')
    return render_template('add_magazine.html')


@app.route('/adminView/adminViewAddAlbum', methods=['POST', 'GET'])
@login_required
@admin_required
def adminViewAddAlbum():
    if request.method == 'POST':
        admin_controller.add_entry_to_catalog(CatalogController.ALBUM_TYPE, request.form)
        flash("Album entry created successfully.", 'success')
        return redirect('viewCatalog')
    return render_template('add_album.html')


@app.route('/adminView/modifyCatalogForm', methods=['GET', 'POST'])
@login_required
@admin_required
def modify_catalog_form():
    type = int(request.form["type"])
    id = request.form['modify_catalog']
    if (type == 1):
        return render_template('modify_book.html', book=admin_controller.get_catalog_entry_by_id(CatalogController.BOOK_TYPE, int(id)))
    if (type == 2):
        return render_template('modify_movie.html', movie=admin_controller.get_catalog_entry_by_id(CatalogController.MOVIE_TYPE, int(id)))
    if (type == 3):
        return render_template('modify_magazine.html', magazine=admin_controller.get_catalog_entry_by_id(CatalogController.MAGAZINE_TYPE, int(id)))
    if (type == 4):
        return render_template('modify_album.html', album=admin_controller.get_catalog_entry_by_id(CatalogController.ALBUM_TYPE, int(id)))


@app.route('/modifyCatalog', methods=['POST'])
@login_required
@admin_required
def modify_catalog():
    type = request.form["type"]
    admin_controller.modify_catalog(type, request.form)
    flash("Entry modified succesfully.", 'success')
    return redirect('viewCatalog')

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
        
    catalog_record = admin_controller.get_catalog_entry_by_id(catalog_type, int(id))
    catalog_record_copy = admin_controller.get_catalog_copies_by_id(catalog_type, int(id))

    return render_template('delete_record_modal.html', catalog_type = int(catalog_type), catalog_record = catalog_record, catalog_record_copy = catalog_record_copy)

@app.route('/deleteCatalog', methods=['POST'])
@login_required
@admin_required
def delete_catalog():

    id = request.form["id"]
    catalog_type = request.form["type"]
    print("Backend ID: " + id)
    admin_controller.delete_catalog_copy_entry(catalog_type, int(id))

    flash("Entry deleted succesfully.", 'success')
    return redirect('viewCatalog')
