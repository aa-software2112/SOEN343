from flask import render_template, g, session, redirect, request, flash
from app import app
from app.common_definitions.helper_functions import login_required
from app import clientController, adminController, catalog_controller
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
    type = int(request.form["catalog_type"])
    if (type == 1):
        filters = catalog_controller.get_filters(CatalogController.BOOK_TYPE)
        sorting_criteria = catalog_controller.get_sorting_criteria(CatalogController.BOOK_TYPE)
        all_records = catalog_controller.get_records_by_catalog(CatalogController.BOOK_TYPE)
        return render_template('view_books.html', records = list(all_records.values()), filters = filters, sorting_criteria = sorting_criteria)

    elif (type == 2):
        filters = catalog_controller.get_filters(CatalogController.MOVIE_TYPE)
        sorting_criteria = catalog_controller.get_sorting_criteria(CatalogController.MOVIE_TYPE)
        all_records = catalog_controller.get_records_by_catalog(CatalogController.MOVIE_TYPE)
        return render_template('view_movies.html', records = list(all_records.values()), filters = filters, sorting_criteria = sorting_criteria)

    elif (type == 3):
        filters = catalog_controller.get_filters(CatalogController.MAGAZINE_TYPE)
        sorting_criteria = catalog_controller.get_sorting_criteria(CatalogController.MAGAZINE_TYPE)
        all_records = catalog_controller.get_records_by_catalog(CatalogController.MAGAZINE_TYPE)
        return render_template('view_magazines.html', records = list(all_records.values()), filters = filters, sorting_criteria = sorting_criteria)

    elif (type == 4):
        filters = catalog_controller.get_filters(CatalogController.ALBUM_TYPE)
        sorting_criteria = catalog_controller.get_sorting_criteria(CatalogController.ALBUM_TYPE)
        all_records = catalog_controller.get_records_by_catalog(CatalogController.ALBUM_TYPE)
        return render_template('view_albums.html', records = list(all_records.values()), filters = filters, sorting_criteria = sorting_criteria)

# To-do - Filters
@app.route('/viewCatalog/search', methods=['GET', 'POST'])
def search():
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
    print("selected record", selected_record)
    return render_template('view_record_details.html', catalog_type = int(catalog_type), record = selected_record)
