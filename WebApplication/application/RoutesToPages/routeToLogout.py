from application import app
from flask import redirect, session, flash, g

@app.route('/logout')
def logout(): 
    if not g.user:
        session.clear()
        flash('Logged out!', 'success')
    return redirect('/index')
