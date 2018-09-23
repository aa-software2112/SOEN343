from flask import render_template
from flask import request
from application import app
from application import userController, adminController
from application import databaseObject as db
import random 

@app.route('/adminCreator')
def createAdminForm():
	return render_template('adminCreator.html')

@app.route('/registerAdmin', methods=['POST'])
def registerAdmin():
	print(request.method)
	for k, v in request.form.items():
		print(k)
		print(v)
	return render_template('adminCreator.html')