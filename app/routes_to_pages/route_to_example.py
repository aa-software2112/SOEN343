from flask import render_template
from app import app
from app import client_controller, admin_controller
from app import databaseObject as db
import random 

@app.route('/example')
def showObject():
	client_controller.example_user_controller_function()
	admin_controller.example_admin_controller_function()
	admin_controller.example_admin_sql_call()
	#this is the object that is going to be sent to the front end
	allLoggedClients = admin_controller.get_all_logged_client()
	# creating a dictionnary object on the fly
	dictionary = {"Title":"TIME", "Publisher":"Time (May 13 2008)", "Language":"English", "ISBN-10":1603200185}
	# rendering the template and setting the objToDisplay in the exampleBackendToFrontend.html to the dictionary
	return render_template('example_backend_to_frontend.html', objToDisplay=dictionary, allLoggedClients= allLoggedClients)

	
