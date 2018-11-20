from flask import render_template, g, session, redirect, request, flash
from app import app
from app.common_definitions.helper_functions import login_required
from app import client_controller, admin_controller, catalog_controller
from app.controllers.catalog_controller import CatalogController

# Needs to be redone
@app.route('/viewCatalog', methods=['GET', 'POST'])
@login_required
def viewCatalog():
    # if g.user["_is_admin"] == 1:
    #     dict_of_catalogs = adminController.view_inventory()
    # else:
    #     dict_of_catalogs = clientController.view_inventory()


    # comment this out when fully implemented
    # for catalog_name in dict_of_catalogs.keys():
    #   print("*****\nDictionary: {}\n*****".format(catalog_name))
    #  dict_of_objects = dict_of_catalogs[catalog_name]
    # for object_id, media_object in dict_of_objects.items():
    #    print ("ID {} OBJ {}".format(object_id, media_object))
    

    return render_template('view_catalog.html')

# Separate the singular view catalog page into its respective page
@app.route('/viewCatalog/viewCatalogTab', methods=['GET', 'POST'])
def viewCatalogTab():
    catalog_type = request.form["catalog_type"]
    url_string=""
    filters = catalog_controller.get_filters(catalog_type)
    sorting_criteria = catalog_controller.get_sorting_criteria(catalog_type)
    all_records = list(catalog_controller.get_records_by_catalog(catalog_type).values())
    if (catalog_type == "1"):
        url_string = "view_books.html"
    elif (catalog_type == "2"):
        url_string = "view_movies.html"
    elif (catalog_type == "3"):
        url_string = "view_magazines.html"
    elif (catalog_type == "4"):
        url_string = "view_albums.html"
    if g.user["_is_admin"] == 1:
        admin_controller.add_list_to(g.user["_id"], all_records)
    else:
        client_controller.add_list_to(g.user["_id"], all_records)

    return render_template(url_string, records=all_records, filters=filters, sorting_criteria=sorting_criteria)

# To-do - Filters
@app.route('/viewCatalog/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        catalog_type = request.form['catalog_type']
        search_value = request.form['search_value']
        url_string =""
        filters = catalog_controller.get_filters(catalog_type)
        transformed_filters = {}
        sorting_criteria = catalog_controller.get_sorting_criteria(catalog_type)
        input_sorting_criteria = request.form['sort_attr']

        for k in filters:
            transformed_filters[k] = request.form[k]

        if (catalog_type == "1"):
            url_string = "view_books.html"
        elif (catalog_type == "2"):
            url_string = "view_movies.html"
        elif (catalog_type == "3"):
           url_string = "view_magazines.html"
        elif (catalog_type== "4"):
            url_string = "view_albums.html"
        if g.user["_is_admin"] == 1:
            search_result = admin_controller.search_from(catalog_type, search_value, g.user["_id"])
            search_result = admin_controller.filter_by(catalog_type, transformed_filters, g.user["_id"])
            search_result = admin_controller.sort_by(catalog_type, input_sorting_criteria, g.user["_id"])
        else:
            search_result = client_controller.search_from(catalog_type, search_value, g.user["_id"])
            search_result = client_controller.filter_by(catalog_type, transformed_filters, g.user["_id"])
            search_result = client_controller.sort_by(catalog_type, input_sorting_criteria, g.user["_id"])

        return render_template(url_string, records = search_result, filters=filters, sorting_criteria = sorting_criteria)

    type = int(request.form["catalog_type"])
    sort_attr = (request.form["sort_attr"])
    print("CatalogType", type)
    print("SortAtt", sort_attr)
    return redirect('viewCatalog')

# View record's detail route. Request the id and catalog_type from the front-end.
@app.route('/viewCatalog/viewDetails', methods=['GET', 'POST'])
def viewDetails():
    type = int(request.form["catalog_type"])
    id = request.form["id"]

    if (type == 1):
        catalog_type = CatalogController.BOOK_TYPE
    elif (type == 2):
        catalog_type = CatalogController.MOVIE_TYPE
    elif (type == 3):
        catalog_type = CatalogController.MAGAZINE_TYPE
    elif (type == 4):
        catalog_type = CatalogController.ALBUM_TYPE

    selected_record = catalog_controller.get_catalog_entry_by_id(catalog_type, int(id))
    if g.user["_is_admin"] == 1:
        admin_controller.set_detailed_view_index(selected_record, g.user["_id"])
    else:
        client_controller.set_detailed_view_index(selected_record, g.user["_id"])
    return render_template('view_record_details.html', catalog_type = int(catalog_type), record = selected_record)

@app.route('/nextDetailedView', methods=['GET', 'POST'])
@login_required
def nextDetailedView():
    if request.method == 'POST':
        catalog_type = request.form["catalog_type"]
        if g.user["_is_admin"] == 1:
            next_catalog_entry = admin_controller.get_next_item(g.user["_id"])
        else:
            next_catalog_entry = client_controller.get_next_item(g.user["_id"])

        return render_template('view_record_details.html', record=next_catalog_entry, catalog_type=int(catalog_type))

@app.route('/backToLIST', methods=['GET', 'POST'])
@login_required
def backToList():
    if request.method == 'POST':
        catalog_type = request.form['catalog_type']
        url_string = ""
        filters = catalog_controller.get_filters(catalog_type)
        sorting_criteria = catalog_controller.get_sorting_criteria(catalog_type)

        if (catalog_type == "1"):
            url_string = "view_books.html"
        elif (catalog_type == "2"):
            url_string = "view_movies.html"
        elif (catalog_type == "3"):
            url_string = "view_magazines.html"
        elif (catalog_type == "4"):
            url_string = "view_albums.html"
        if g.user["_is_admin"] == 1:
            last_searched_list = admin_controller.get_last_searched_list(g.user["_id"])
        else:
            last_searched_list = client_controller.get_last_searched_list(g.user["_id"])

    return render_template(url_string, records=last_searched_list, filters=filters, sorting_criteria=sorting_criteria)


@app.route('/deleteCart', methods=['POST'])
@login_required
def delete_cart():
    #get the id of item to be deleted
    o_id = request.form["id"]
    user_id = g.user["_id"]
    current_cart = client_controller.delete_from_cart(o_id, user_id)
    flash("Deleted successfully.", 'success')
    return render_template('view_cart.html', current_cart=current_cart)
