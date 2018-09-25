from flask import render_template
from application import app
from application import userController, adminController
from application import databaseObject as db
import random 

@app.route('/adminView')
def adminView():

	return render_template('administratorView.html')

	
@app.route('/adminView/adminCreator')
def adminCreator():

	return render_template('administratorCreator.html')
	
@app.route('/adminView/adminViewUserRegistry')
def adminViewUserRegistry():

	allLoggedClients = adminController.getAllLoggedClient()
	return render_template('administratorViewUserRegistry.html', allLoggedClients = allLoggedClients)
	
@app.route('/adminView/adminViewRecords')
def adminViewRecords():
	
	return render_template('administratorViewRecords.html')
	
@app.route('/adminView/adminViewCatalog')
def adminViewCatalog():
	
	return render_template('administratorViewCatalog.html')
	
	
	