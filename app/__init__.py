import os
from flask import Flask

app = Flask(__name__)

# Dynamically generates the routes.py file
with open('app/routes.py', 'w') as file:
    file.write("from flask import render_template\nimport random\n\n# All routes from route folder are imported here...\n")

    for route in os.listdir("app/routes_to_pages"):
        file.write("from app.routes_to_pages import {}\n".format(route.split('.')[0]))
        print("Added {}".format(route))

"""
 Order of imports with description:
1. DatabaseContainer Class for storing/abstracting the sqlite object for use in all routes
2. The path needed to initialize the database in the correct folder
3. The SQLite initialization script for creating the database with sufficient entries for testing
4. The Controller directory that has all controller classes 
5. Imports all routes to be used by the application (app)
6. Imports the catalog controller that controls all catalog-based transactions
"""
from app.classes.database_container import DatabaseContainer
from app.common_definitions.common_paths import PATH_TO_DATABASE
from app.database import sqlite_script
from app.controllers.user_controller import UserController
from app.controllers.admin_controller import AdminController
from app.controllers.catalog_controller import CatalogController

# Create and fill database with values - closes connection to 
sqlite_script.initializeAndFillDatabase(PATH_TO_DATABASE)

# Connect to the database through an abstracted object - this object must be imported into route files for use
databaseObject = DatabaseContainer(PATH_TO_DATABASE)

# Send the database object to all Controllers
catalog_controller = CatalogController(databaseObject)
catalog_controller.load_database_into_memory()

userController = UserController(databaseObject)
adminController = AdminController(databaseObject, catalog_controller)

from app import routes