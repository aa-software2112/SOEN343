from flask import Flask,render_template, redirect, session, flash, make_response, g, request
from application import app
from application import userController
from application.Classes.forms import LoginForm

app.config['SECRET_KEY'] = 'SOEN_343'

# Declaring variable
client_response = ""
client_to_log = {
	"username": "",
	"password": ""
}

# Login Template
@app.route('/login', methods=['GET', 'POST'])
def login():

	# import from Classes/forms
	form = LoginForm()	
	
	if form.validate_on_submit():
		global client_response
		global client_to_log

		get_username = form.username.data
		get_password = form.password.data
		# Return query result
		client_response = userController.getClientByPassword(username=get_username, password=get_password)
		# Temporary. Waiting to perform the right query for log in		

		if client_response is None: 
			error = "Username not found"
			return render_template('login.html', form=form, error=error)

		else: 
			for client in client_response:
				client_to_log = {
					"username": client.username,
					"password": client.password
				}
			
			# [To-do] Add encryption
			if client_to_log["password"] == get_password:

				# Set session
				session.clear() 	# The user will not have access to the login page while logged, but the session will be reset just in case
				session['logged_in'] = True
				session['user'] = client_to_log["username"]

				# Display message after being redirected to home page
				flash('You are now logged in!', 'success')

				# Set cookies.
				resp =  make_response(redirect('/index'))
				resp.set_cookie('username', get_username)
				return resp
			else:
				# Invalid username or password
				error = "Invalid login. Please check your username or password"
				return render_template('login.html', form=form, error=error)
	
	return render_template('login.html', form=form)

# Session and cookies are set as in global variable g, before requesting any route
@app.before_request
def remember_user():
	user = session.get('user')
	if user is None:
		g.user = None
		g.username = None
	else:
		g.user = session['user']
		g.username = request.cookies.get('username')

