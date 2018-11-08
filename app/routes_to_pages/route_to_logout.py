from app import app
from flask import redirect, session, flash, g, make_response, url_for
from app import clientController, adminController


@app.route('/logout')
def logout():
    if g.user['_is_admin'] == 1:
        adminController.logout_admin(g.user["_username"])

    else:
        clientController.logout_client(g.user["_username"])
    session.clear()
    flash('Logged out!', 'success')

    return redirect(url_for('index'))
