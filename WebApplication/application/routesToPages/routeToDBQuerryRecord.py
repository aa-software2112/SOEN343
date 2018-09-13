from flask import render_template
from application import app
from application.models import User
import random


@app.route('/Select')
def showUser():
    # Querrying from database
    try:
        u = User.query.all()
        for user in u:
            print(user.fname)

    except:
        print('Error selecting')

    return render_template('dbExample.html', objToDisplay=u)