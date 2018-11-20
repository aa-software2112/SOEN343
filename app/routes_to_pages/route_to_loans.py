from flask import render_template, request, g, redirect
from app import app
from app.common_definitions.helper_functions import login_required
from app import client_controller


@app.route('/myLoans')
@login_required
def my_loans():
	"""Function that get the user's loans and display them on a page"""


	user_loans = client_controller.get_loaned_items(g.user["_id"])

	if len(user_loans) == 0:
		err = "There are no items to return"
	else:
		err = None

	return render_template('my_loans.html', loans=user_loans, errorMessage=err)


@app.route('/returnLoans', methods=['POST'])
def return_loans():

	#returns the id(selected) as a list
	return_items_id = request.form.getlist('id')

	client_controller.return_loaned_items(return_items_id, g.user["_id"])
	err = None
	if len(return_items_id) == 0 :
		err = "Please, select items to return"
	return render_template('return_loans.html', error=err)