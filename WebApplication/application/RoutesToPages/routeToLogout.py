from application import app
from flask import redirect, session, flash, g, make_response

@app.route('/logout')
def logout(): 
    if g.user:
        session.clear()
        flash('Logged out!', 'success')
    return redirect('/index')
        

