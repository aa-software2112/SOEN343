from flask import Flask, render_template, redirect, session, flash, make_response, g, request, url_for
from app import app
from app import clientController, adminController
from app.classes.forms import LoginForm
from app.common_definitions.helper_functions import is_logged

import json

app.config['SECRET_KEY'] = 'SOEN_343'


# Login Template
@app.route('/login', methods=['GET', 'POST'])
@is_logged
def login():

    # import from Classes/forms
    form = LoginForm()

    if form.validate_on_submit():

        get_username = form.username.data
        get_password = form.password.data
        # Return query result
        user_response = clientController.get_client_by_password(
            username=get_username, password=get_password) + adminController.get_admin_by_password(username=get_password,
                                                                                                  password=get_password)

        if user_response == []:
            error = "Invalid login. Please check your username or password"
            return render_template('login.html', form=form, error=error)

        else:
            client = user_response[0]

            # Set session
            session.clear() 	# The user will not have access to the login page while logged, but the session will be reset just in case
            session['logged_in'] = True
            session['user'] = client.__dict__

            # Display message after being redirected to home page
            flash('You are now logged in!', 'success')

            return redirect(url_for('index'))

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
