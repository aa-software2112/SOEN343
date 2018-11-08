from flask import render_template, g, session, redirect, request, flash
from app import app
from app.common_definitions.helper_functions import login_required
from app import clientController, adminController

@app.route('/detailedView', methods=['GET', 'POST'])
@login_required
def detailedView():
    item_id = request.form["id"]
    catalog_type = request.form["type"]
    if g.user["_is_admin"] == 1:
        catalog_entry = adminController.get_catalog_entry_by_id(catalog_type, int(item_id))
    else:
        catalog_entry = clientController.get_catalog_entry_by_id(catalog_type, int(item_id))

    #uncomment  when template for detailed view is defined
    #return render_template('detailed_view.html', catalog_entry=catalog_entry)

@app.route('/nextDetailedView', methods=['GET', 'POST'])
@login_required
def nextDetailedView():
    if g.user["_is_admin"] == 1:
        next_catalog_entry = adminController.get_next_item(g.user["_id"])
    else:
        next_catalog_entry = clientController.get_next_item(g.user["_id"])

    #uncomment  when template for detailed view is defined
    #return render_template('detailed_view.html', next_catalog_entry=next_catalog_entry)

@app.route('/backToLIST', methods=['GET', 'POST'])
@login_required
def backToList():
    if g.user["_is_admin"] == 1:
        last_searched_list = adminController.get_last_searched_list(g.user["_id"])
    else:
        last_searched_list = clientController.get_last_searched_list(g.user["_id"])

    #uncomment  when template for back view is defined
    #return render_template('searched_list_view.html', last_searched_list=last_searched_list)