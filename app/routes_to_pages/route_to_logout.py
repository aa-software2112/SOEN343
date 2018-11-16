from app import app
from flask import redirect, session, flash, g, make_response, url_for
from app import client_controller, admin_controller


@app.route('/logout')
def logout():
    if g.user['_is_admin'] == 1:
        admin_controller.logout_admin(g.user["_username"])

    else:
        client_controller.logout_client(g.user["_username"])
    session.clear()
    flash('Logged out!', 'success')

    return redirect(url_for('index'))
