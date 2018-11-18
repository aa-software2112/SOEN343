from flask import render_template, request

from app import app
from app.common_definitions.helper_functions import login_required


@app.route('/myLoans')
@login_required
def my_loans():
	"""Function that get the user's loans and display them on a page"""
	# get loans, these are temporary example while the loan logic gets implemented
	loan1 = {'_id': 1, '_name': 'My first loan'}
	loan2 = {'_id': 2, '_name': 'My second loan'}
	loan3 = {'_id': 3, '_name': 'My third loan'}
	user_loans = [loan1, loan2, loan3]
	err = None
	if len(user_loans) == 0:
		err = "You have no loans on record"
	return render_template('my_loans.html', loans=user_loans, errorMessage=err)


@app.route('/returnLoans', methods=['POST'])
def return_loans():
	# do logic to return the loans
	data = request.form
	print(data)
	return render_template('return_loans.html')