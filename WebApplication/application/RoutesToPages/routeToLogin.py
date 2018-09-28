from flask import Flask,render_template, redirect, session, flash, make_response, g, request
from application import app
from application import userController
from application.Classes.forms import LoginForm

app.config['SECRET_KEY'] = 'SOEN_343'


# Login Template
@app.route('/login', methods=['GET', 'POST'])
def login():

	# import from Classes/forms
	form = LoginForm()	
	# Declaring variable
	client_response = ""

	if form.validate_on_submit():

		get_username = form.username.data
		get_password = form.password.data
		# Return query result
		client_response = userController.getClientByPassword(username=get_username, password=get_password)

		if client_response == []: 
			error = "Invalid login. Please check your username or password"
			return render_template('login.html', form=form, error=error)

		else: 
			client = client_response[0]
		
			# Set session
			session.clear() 	# The user will not have access to the login page while logged, but the session will be reset just in case
			session['logged_in'] = True
			session['user'] = client.username

			# Display message after being redirected to home page
			flash('You are now logged in!', 'success')

			return redirect('/index')
			
	return render_template('login.html', form=form)

# Session and cookies are set as in global variable g, before requesting any route
@app.before_request
def remember_user():
	user = session.get('user')
	if user is None:
		g.user = None
	else:
		g.user = session['user']

