from flask import render_template
from flask import request
from application import app
from application import userController, adminController
from application import databaseObject as db
import random 

@app.route('/clientSignup')
def clientSignup():
	return render_template('clientSignup.html')

@app.route('/signupForm', methods=['POST'])
def processSignup():
	print(request.method)
	for k, v in request.form.items():
		print(k)
		print(v)
	return render_template('clientSignup.html')