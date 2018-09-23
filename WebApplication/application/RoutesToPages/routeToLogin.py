from flask import Flask,render_template, redirect
from application import app
from application import userController
from application.Classes.forms import LoginForm, RegistrationForm

app.config['SECRET_KEY'] = 'SOEN_343'

user_mock = {
	"id": 2,
	"firstName": "Jasonn",
	"lastName": "Jasonnnn",
	"physicalAddress": "4305 Somewhere",
	"email": "jason@email.com",
	"phoneNumber": "514-555-5555",
	"username": "secretname",
	"password": "superpassword",
	"isAdmin": 1,
	"isLogged": 1
}

# Login Template
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()	
	clients_login_info = userController.loginHandler()
	if form.validate_on_submit():
		# return '<h1>' +  form.username.data + ' ' + form.password.data + '</h1>'
		user = user_mock
		if user: 
			if user["password"] == form.password.data:
				return redirect('/index')
		return '<h1> Invalid username or password </h1>'
	return render_template('login.html', form=form, clients_login_info=clients_login_info)
