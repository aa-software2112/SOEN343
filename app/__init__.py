import os
from flask import Flask

app = Flask(__name__)

# Dynamically generates the routes.py file
with open('app/routes.py', 'w') as file:
    file.write("from flask import render_template\nimport random\n\n# All routes from route folder are imported here...\n")

    for route in os.listdir("app/routes_to_pages"):
        file.write("from app.routes_to_pages import {}\n".format(route.split('.')[0]))
        print("Added {}".format(route))

from app.classes.database_container import DatabaseContainer
from app.common_definitions.common_paths import PATH_TO_DATABASE
from app.database import sqlite_script
from app.controllers.user_controller import ClientController
from app.controllers.admin_controller import AdminController
from app.controllers.catalog_controller import CatalogController
from app.common_definitions import helper_functions

# Create and fill database with values - closes connection to 
sqlite_script.initializeAndFillDatabase(PATH_TO_DATABASE)

# Connect to the database through an abstracted object - this object must be imported into route files for use
databaseObject = DatabaseContainer(PATH_TO_DATABASE)

# Send the database object to all Controllers
catalog_controller = CatalogController(databaseObject)
catalog_controller.load_database_into_memory()

clientController = ClientController(databaseObject)
clientController.load_database_into_memory()

adminController = AdminController(databaseObject, catalog_controller)
adminController.load_database_into_memory()

# Helper function to be used in front end
app.jinja_env.globals.update(convert_epoch_to_datetime=helper_functions.convert_epoch_to_datetime)

from app import routes