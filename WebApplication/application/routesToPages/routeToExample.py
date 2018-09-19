from flask import render_template
from application import app
from application import databaseObject as db
from application.Manipulators import UserManipulator, AdminManipulator
import random 

@app.route('/example')
def showObject():
	UserManipulator.exampleUserManipulatorFunction()
	AdminManipulator.exampleAdminManipulatorFunction()
	# creating a dictionnary object on the fly
	dictionary = {"Title":"TIME", "Publisher":"Time (May 13 2008)", "Language":"English", "ISBN-10":1603200185}
	# rendering the template and setting the objToDisplay in the exampleBackendToFrontend.html to the dictionary
	return render_template('exampleBackendToFrontend.html', objToDisplay=dictionary)

	
