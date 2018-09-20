from flask import Flask,render_template, redirect, flash, session, make_response
from application import app
from application.Classes.forms import LoginForm, RegistrationForm

app.config['SECRET_KEY'] = 'SOEN_343'

# https://www.tutorialspoint.com/flask/flask_cookies.htm
@app.route('/setCookie', methods=['GET', 'POST'])
def setCookie():
    form = LoginForm()
    userEmail = form.email.data

    resp = make_response(redirect('/index'))
    resp.set_cookie('userEmail', userEmail)
    return resp
	

