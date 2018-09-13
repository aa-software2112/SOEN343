from flask import render_template
from application import app
from application.models import User
from application import db
from flask import redirect
import random


@app.route('/delete/<string>')
def deleteUser(string):
    # Delteing from database
    try:
        check= User.query.filter_by(fname=string).first()
        if check is None:
            return render_template('dbNoEntryFound.html', objToDisplay=string)
        else:
            db.session.delete(check)
            db.session.commit()

    except:
        print('Error deleting')

    return redirect('/Select')