from flask import render_template, g, session, redirect, request,flash
from application import app
from application import userController, adminController
from application import databaseObject as db
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



	
