from flask import Flask,render_template, redirect
from application import app
from application.Classes.forms import LoginForm, RegistrationForm

app.config['SECRET_KEY'] = 'SOEN_343'

# Login Template
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()	
	if form.validate_on_submit():
		return redirect('/index')
	return render_template('login.html', form=form)
