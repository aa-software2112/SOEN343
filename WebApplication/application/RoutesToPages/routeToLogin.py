from flask import Flask,render_template, redirect, session, flash, make_response
from application import app
from application import userController
from application.Classes.forms import LoginForm, RegistrationForm

app.config['SECRET_KEY'] = 'SOEN_343'

# Login Template
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()	
	clients_login = userController.loginHandler()
	session.pop('user', None)
	if form.validate_on_submit():
		# return '<h1>' +  form.username.data + ' ' + form.password.data + '</h1>'
		
		for x in clients_login:
			user = {
				"username": x.username,
				"password": x.password
			}

		print(user["password"])

		if user: 
			if user["password"] == form.password.data:
				session['logged_in'] = True
				session['user'] = user["username"]
				flash('You are now logged in!', 'success')

				resp =  make_response(redirect('/index'))
				resp.set_cookie('username', form.username.data)
				return resp
			else:
				error = "Invalid login"
				return render_template('login.html', form=form, error=error)
		else: 
			error = "Username not found"
			return render_template('login.html', form=form, error=error)

	return render_template('login.html', form=form, clients_login=clients_login)


