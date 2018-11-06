from flask import render_template, g, session, redirect, request, flash
from app import app
from app.common_definitions.helper_functions import login_required
from app import clientController, adminController, catalog_controller
from app.controllers.catalog_controller import CatalogController

@app.route('/viewCatalog', methods=['GET', 'POST'])
@login_required
def viewCatalog():
    if g.user["_is_admin"] == 1:
        dict_of_catalogs = adminController.view_inventory()
    else:
        dict_of_catalogs = clientController.view_inventory()
    # comment this out when fully implemented
    # for catalog_name in dict_of_catalogs.keys():
    #   print("*****\nDictionary: {}\n*****".format(catalog_name))
    #  dict_of_objects = dict_of_catalogs[catalog_name]
    # for object_id, media_object in dict_of_objects.items():
    #    print ("ID {} OBJ {}".format(object_id, media_object))
    
    # Load the catalog filters when the viewCatalog page loads
    book_filters = catalog_controller.get_filters(CatalogController.BOOK_TYPE)
    movie_filters = catalog_controller.get_filters(CatalogController.MOVIE_TYPE)
    magazine_filters = catalog_controller.get_filters(CatalogController.MAGAZINE_TYPE)
    album_filters = catalog_controller.get_filters(CatalogController.ALBUM_TYPE)

    return render_template('view_catalog.html', 
        dict_of_catalogs=dict_of_catalogs, 
        book_filters = book_filters,
        movie_filters = movie_filters,
        magazine_filters = magazine_filters,
        album_filters = album_filters
    )

# @app.route('/viewCatalog/getSearchFilters', methods=['GET', 'POST'])
# def getCatalogType():
#     type = int(request.form["catalog_type"])
#     print("CatalogType", type)
#     test = "Testing"
#     render_template('includes/book_search_box.html', test=test)
#     return redirect('viewCatalog')
