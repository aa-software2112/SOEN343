from functools import wraps
from flask import g, redirect, request, url_for

def admin_required(f):
    @wraps(f)
    def check_admin(*args, **kwargs):
        # if the user isn't an admin, redirect to the home page, else the function has access to g.user
        if g.user["isAdmin"]:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('index'))
    return check_admin