from application import app
from flask import redirect, session, flash, g, make_response, url_for
from application import userController

@app.route('/logout')
def logout(): 
    if g.user:
        userController.logoutClient(g.user["username"])
        session.clear()
        flash('Logged out!', 'success')
    return redirect(url_for('index'))
        

