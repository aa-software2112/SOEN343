from flask import render_template, g, session, redirect
from application import app
from application import userController, adminController
from application import databaseObject as db
import random 

@app.route('/adminView')
def adminView():
	if g.user:
		return render_template('administratorView.html')
	return redirect('/index')

@app.route('/adminView/adminCreator')
def adminCreator():

	return render_template('administratorCreator.html')
	
@app.route('/adminView/adminViewUserRegistry')
def adminViewUserRegistry():

	return render_template('administratorViewUserRegistry.html')
	
@app.route('/adminView/adminViewRecords')
def adminViewRecords():
	
	return render_template('administratorViewRecords.html')
	
@app.route('/adminView/adminViewCatalog')
def adminViewCatalog():
	
	return render_template('administratorViewCatalog.html')
	
@app.before_request
def before_request():
	g.user = None
	if 'user' in session:
		g.user = session['user']

	