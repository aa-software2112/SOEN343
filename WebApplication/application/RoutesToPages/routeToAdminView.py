from flask import render_template, g, session, redirect, request,flash
from application import app
from application import userController, adminController
from application import databaseObject as db
from application.Classes.Book import Book
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
	
@app.route('/adminView/adminViewRecords')
def adminViewRecords():

	return render_template('administratorViewRecords.html')
	
@app.route('/adminView/adminViewCatalog')
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


@app.route('/adminView/modifyBook')
def modifyBook():
    return render_template('modifyBook.html')

@app.route('/adminView/adminViewAddBook', methods=['POST', 'GET'])
def adminViewAddBook():
	catalog_item={}

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

		catalog_item = {
			'id': 544,
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


		adminController.add_new_book(catalog_add_item=catalog_item)
	


	return render_template('addBook.html')

@app.route('/adminView/adminViewAddMagazine', methods=['POST', 'GET'])
def adminViewAddMagazine():
	catalog_item={}

	if request.method == 'POST':
		_title = request.form.get('title')
		_publisher = request.form.get('publisher')
		_year_of_publication = request.form.get('year_of_publication')
		_language = request.form.get('language')
		_isbn_10 = request.form.get('isbn_10')
		_isbn_13 = request.form.get('isbn_13')

		catalog_item = {
			'id': 544,
			'title': _title,
			'publisher': _publisher,
			'year_of_publication': _year_of_publication,
			'language': _language,
			'isbn_10': _isbn_10,
			'isbn_13': _isbn_13
		}


		adminController.add_new_magazine(catalog_add_item=catalog_item)
	


	return render_template('addMagazine.html')

@app.route('/adminView/adminViewAddalbum', methods=['POST', 'GET'])
def adminViewAddalbum():
    catalog_item = {}

    if request.method == 'POST':
        _type = request.form.get('type')
        _title = request.form.get('title')
        _artist = request.form.get('artist')
        _label = request.form.get('label')
        _release_date = request.form.get('release_date')
        _asin = request.form.get('asin')


        catalog_item = {
            'id': 544,
            'type': _type,
            'title': _title,
            'artist': _artist,
            'label': _label,
            'release_date': _release_date,
            'asin': _asin,

        }
        flash("Entry Created Successfully!!", 'success')


        adminController.add_new_album(catalog_add_item=catalog_item)

    return render_template('AddAlbum.html')










