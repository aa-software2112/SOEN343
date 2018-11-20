from flask import render_template, request, g, redirect
from app import app
from app.common_definitions.helper_functions import login_required, admin_required, convert_epoch_to_datetime
from app import client_controller, catalog_controller, admin_controller
from app.classes.loan import Loan



@app.route('/myLoans')
@login_required
def my_loans():
	"""Function that get the user's loans and display them on a page"""


	#user_loans = client_controller.get_loaned_items(g.user["_id"])
	loan1 = Loan(client_controller.get_client_by_username('antman')[0],
				 catalog_controller.get_catalog_entry_by_id("1", 1))
	loan2 = Loan(admin_controller.get_admin_by_username('catwoman')[0],
				 catalog_controller.get_catalog_entry_by_id("2", 1))
	user_loans = [loan1,loan2]

	if len(user_loans) == 0:
		err = "There are no items to return"
	else:
		err = None

	return render_template('my_loans.html', loans=user_loans, errorMessage=err)


@app.route('/returnLoans', methods=['POST'])
def return_loans():

	print(request.form)
	#returns the id(selected) as a list
	return_items_id = request.form.getlist('id')

	client_controller.return_loaned_items(return_items_id, g.user["_id"])
	err = None
	if len(return_items_id) == 0 :
		err = "Please, select items to return"
	return render_template('return_loans.html', error=err)

@app.route('/transactionHistory')
@login_required
@admin_required
def display_loans():
	# loan used for testing the feature, while waiting for get all loans as list
	loan1 = Loan(client_controller.get_client_by_username('antman')[0],catalog_controller.get_catalog_entry_by_id("1",1))
	loan2 =Loan(admin_controller.get_admin_by_username('catwoman')[0],catalog_controller.get_catalog_entry_by_id("2",1))

	return render_template('transaction_history.html', epoch_converter=convert_epoch_to_datetime,
						   loan_history=[loan1, loan2])