from flask import render_template
from application import app
from application import db
from application.models import User
import random

@app.route('/insert/<string>')
def insertUser(string):
    # inserting a record to database
    try:
        user = User(fname=string)
        db.session.add(user)
        db.session.commit()
        print(string + 'inserted to databse correctly')
    except:
        print('Error inserting')

    return "Prompt"