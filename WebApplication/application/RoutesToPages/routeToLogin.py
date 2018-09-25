from flask import Flask,render_template, redirect, session, flash, make_response, g, request
from application import app
from application import userController
from application.Classes.forms import LoginForm, RegistrationForm

app.config['SECRET_KEY'] = 'SOEN_343'

# Declaring variable
clients_login = ""
check_client = {
	"username": "",
	"password": ""
}
# Login Template
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()	

	# The user will not have access to the login page while logged, but the session will be reset just in case
	session.pop('user', None)
	
	if form.validate_on_submit():
		global clients_login
		global check_client

		get_username = form.username.data
		get_password = form.password.data
		# Return query result
		clients_login = userController.getClientByPassword(username=get_username, password=get_password)
		# Temporary. Waiting to perform the right query for log in		

		if clients_login is None: 
			error = "Username not found"
			return render_template('login.html', form=form, error=error)
			# [To-do] Add encryption
		else: 
			for x in clients_login:
				check_client = {
					"username": x.username,
					"password": x.password
				}
			
			if check_client["password"] == get_password:

				# Set session
				session.clear()
				session['logged_in'] = True
				session['user'] = check_client["username"]

				# Display message after being redirected to home page
				flash('You are now logged in!', 'success')

				# Set cookies.
				resp =  make_response(redirect('/index'))
				resp.set_cookie('username', form.username.data)
				return resp
			else:
				# Invalid password
				error = "Invalid login. Please check your username or password"
				return render_template('login.html', form=form, error=error)
			
	return render_template('login.html', form=form, clients_login=clients_login)

# After login in, the user is redirected to the index page. Before that, session and cookies are set as in global
# variable g, before requesting the index route
@app.before_request
def remember_user():
	user = session.get('user')
	if user is None:
		g.user = None
		g.username = None
	else:
		g.user = session['user']
		g.username = request.cookies.get('username')

