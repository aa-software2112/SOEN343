from flask import Flask,render_template, redirect, session, flash, make_response, g, request
from application import app
from application import userController
from application.Classes.forms import LoginForm, RegistrationForm

app.config['SECRET_KEY'] = 'SOEN_343'

# Declaring variable
clients_login = ""

# Login Template
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()	

	# The user will not have access to the login page while logged, but the session will be reset just in case
	session.pop('user', None)
	
	if form.validate_on_submit():
		global clients_login

		get_username = form.username.data
		get_password = form.password.data
		# Return query result
		clients_login = userController.loginHandler(username=get_username)
		# Temporary. Waiting to perform the right query for log in		
		for x in clients_login:
			user = {
				"username": x.username,
				"password": x.password
			}

		if user: 
			# [To-do] Add encryption
			if user["password"] == get_password:

				# Set session
				session['logged_in'] = True
				session['user'] = user["username"]

				# Display message after being redirected to home page
				flash('You are now logged in!', 'success')

				# Set cookies.
				resp =  make_response(redirect('/index'))
				resp.set_cookie('username', form.username.data)
				return resp
			else:
				# Invalid password
				error = "Invalid login"
				return render_template('login.html', form=form, error=error)
		else: 
			error = "Username not found"
			return render_template('login.html', form=form, error=error)

	return render_template('login.html', form=form, clients_login=clients_login)

# After login in, the user is redirected to the index page. Before that, session and cookies are set as in global
# variable g, before requesting the index route
@app.before_request
def before_request():
	g.user = None
	g.username = None
	if 'user' in session:
		g.user = session['user']
		g.username = request.cookies.get('username')