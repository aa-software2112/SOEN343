from flask import render_template
from application import app
from application import userController, adminController
from application import databaseObject as db
import random 

@app.route('/clientSignup')
def clientSignup():
	return render_template('clientSignup.html')