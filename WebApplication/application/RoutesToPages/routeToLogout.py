from application import app
from flask import redirect, session, flash, g, make_response

@app.route('/logout')
def logout(): 
    if g.user:
        session.clear()
        resp = make_response(redirect('/index'))
        resp.set_cookie('username', expires=0 )
        flash('Logged out!', 'success')
        return resp
        

