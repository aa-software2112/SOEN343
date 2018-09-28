from application import app
from flask import redirect, session, flash, g, make_response
from application import userController

@app.route('/logout')
def logout(): 
    if g.user:
        userController.logoutClient(g.user)
        session.clear()
        flash('Logged out!', 'success')
    return redirect('/index')
        

