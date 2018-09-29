from flask import render_template, g, session, redirect, request
from application import app
from application import userController, adminController
from application import databaseObject as db
import random
import ctypes  #

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
	
	return render_template('administratorViewCatalog.html')

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


        userController.createClient(firstname, lastname, address, phonenumber, email, username, password, typeofclient, 0, 0)
        ctypes.windll.user32.MessageBoxW(0, "Registration Confirm!!! ", "New Client Registered  ", 1)
        return redirect("/")
    else:
        print("User already exist in database")
        ctypes.windll.user32.MessageBoxW(0, "Select different username or emailaddress  ", "Username/email address already exist ", 1)
        return redirect("/adminView/userCreator")



	
