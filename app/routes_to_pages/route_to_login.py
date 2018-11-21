from flask import Flask, render_template, redirect, session, flash, make_response, g, request, url_for
from app import app
from app import client_controller, admin_controller
from app.classes.forms import LoginForm
from app.common_definitions.helper_functions import is_logged
import time

app.config['SECRET_KEY'] = 'SOEN_343'


# Login Template
@app.route('/login', methods=['GET', 'POST'])
@is_logged
def login():

    print(request.form)
    print(session)

    # import from Classes/forms
    form = LoginForm()

    if form.validate_on_submit():

        get_username = form.username.data
        get_password = form.password.data
        # Return query result
        user_response = client_controller.get_client_by_password(
            username = get_username, password=get_password) + admin_controller.get_admin_by_password(username=get_username,
                                                                                                     password=get_password)

        if not user_response:
            error = "Invalid login. Please check your username or password"
            return render_template('login.html', form=form, error=error)

        else:
            user = user_response[0]

            if user._is_admin == 1:
                admin_controller.login_admin(get_username)
            else:
                client_controller.login_client(get_username)


            # Set session.
            # The user will not have access to the login page while logged, but the session will be reset just in case.
            session.clear()
            session['logged_in'] = True

            # Do not send cart object to front end, i.e. pop it from the dict stored in user session.
            session['user'] = vars(user).copy()
            session['user'] = user.get_session_dict()

            # Display message after being redirected to home page.
            print(session)
            flash('You are now logged in!', 'success')

            return redirect(url_for('viewCatalog'))

    return render_template('login.html', form=form)

# Session and cookies are set as in global variable g, before requesting any route
# To access session -> ex: g.user["param"]


@app.before_request
def remember_user():
    user = session.get('user')

    if user is None:
        g.user = None
    else:
        g.user = (session['user'])
