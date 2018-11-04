from app import app
from flask import redirect, session, flash, g, make_response, url_for
from app import clientController


@app.route('/logout')
def logout():
    if g.user:
        clientController.logout_client(g.user["username"])
        session.clear()
        flash('Logged out!', 'success')
    return redirect(url_for('index'))
