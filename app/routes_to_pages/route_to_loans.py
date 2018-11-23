from flask import render_template, request, g, redirect
from app import app
from app.common_definitions.helper_functions import login_required, admin_required, convert_epoch_to_datetime
from app import client_controller, catalog_controller, admin_controller
from app.classes.loan import Loan

from app.common_definitions.helper_functions import convert_epoch_to_datetime as to_datetime

@app.route('/myLoans', methods = ['GET', 'POST'])
@login_required
def my_loans():
	"""Function that get the user's loans and display them on a page"""

	# tested with these
	# loan1 = Loan(client_controller.get_client_by_username('antman')[0],
	# 			 catalog_controller.get_catalog_entry_by_id("1", 1))
	# loan2 = Loan(admin_controller.get_admin_by_username('catwoman')[0],
	# 			 catalog_controller.get_catalog_entry_by_id("2", 1))
	# user_loans = [loan1,loan2]

	client_id = g.user['_id']

	# I'm expecting a list of loan objects with this
	user_loans = client_controller.get_loaned_items(client_id)

	if len(user_loans) == 0:
		err = "There are no items to return"
	else:
		err = None

	return render_template('my_loans.html', loans=user_loans, errorMessage=err)


@app.route('/returnLoans', methods=['POST'])
def return_loans():

	# get the list of loan ids from the form
	return_items_id = request.form.getlist('id')

	# tested with this
	# loan1 = Loan(client_controller.get_client_by_username('antman')[0],
	# 			 catalog_controller.get_catalog_entry_by_id("1", 1))
	# loan2 = Loan(admin_controller.get_admin_by_username('catwoman')[0],
	# 			 catalog_controller.get_catalog_entry_by_id("2", 1))

	# casting the string values to integer
	return_items_id = [int(i) for i in return_items_id]
	client_id = g.user['_id']

	# I'm expecting a list of loan objects here; non-returned loans
	non_returned_items = client_controller.return_loaned_items(return_items_id, client_id)

	err = ""

	if len(non_returned_items) > 0:
		for non_returned_item in non_returned_items:
			err += non_returned_item.get_record_title() + ", "
		err += " couldn't be returned."


	return render_template('return_loans.html', err = err)
