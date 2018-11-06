from flask import render_template, g, session, redirect, request, flash
from app import app
from app.common_definitions.helper_functions import login_required
from app import clientController, adminController

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

    return render_template('view_catalog.html', dict_of_catalogs=dict_of_catalogs)

@app.route('/viewCatalog/getSearchFilters', methods=['GET', 'POST'])
def getCatalogType():
    type = int(request.form["catalog_type"])
    print("CatalogType", type)
    return redirect('/viewCatalog')

