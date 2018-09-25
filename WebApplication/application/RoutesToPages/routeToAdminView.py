from flask import render_template
from flask import request
from application import app
from application import userController, adminController
from application import databaseObject as db
import random 

@app.route('/adminView')
def adminView():

	return render_template('administratorView.html')

	
@app.route('/adminView/userCreator')
def userCreator():

	return render_template('userCreator.html')
	
@app.route('/adminView/adminViewUserRegistry')
def adminViewUserRegistry():

	return render_template('administratorViewUserRegistry.html')
	
@app.route('/adminView/adminViewRecords')
def adminViewRecords():
	
	return render_template('administratorViewRecords.html')
	
@app.route('/adminView/adminViewCatalog')
def adminViewCatalog():
	
	return render_template('administratorViewCatalog.html')

@app.route('/registerUser', methods=['POST'])
def registerAdmin():
	print(request.method)
	for k, v in request.form.items():
		print(k)
		print(v)
	return render_template('userCreator.html')
	
	
	