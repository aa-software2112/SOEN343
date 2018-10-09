from application.AutomationFiles.generateRoutesDotPy import generateRoutesFile as genRoutePy 

# Generates the routes.py file
genRoutePy()

# Sets up the application for running
from flask import Flask

app = Flask(__name__)

"""
 Order of imports with description:
1. DatabaseContainer Class for storing/abstracting the sqlite object for use in all routes
2. The path needed to initialize the database in the correct folder
3. The SQLite initialization script for creating the database with sufficient entries for testing
4. The Controller directory that has all controller classes 
5. Imports all routes to be used by the application (app)
6. Imports the catalog controller that controls all catalog-based transactions

 """
from application.Classes.DatabaseContainer import DatabaseContainer
from application.CommonDefinitions.CommonPaths import PATH_TO_DATABASE
from application.Database import SQLiteScript
from application.Controllers.UserController import UserController
from application.Controllers.AdminController import AdminController
from application.Controllers.CatalogController import CatalogController

# Create and fill database with values - closes connection to 
SQLiteScript.initializeAndFillDatabase(PATH_TO_DATABASE)

# Connect to the database through an abstracted object - this object must be imported into route files for use
databaseObject = DatabaseContainer(PATH_TO_DATABASE)

# Send the database object to all Controllers
catalog_controller = CatalogController(databaseObject)
catalog_controller.load_database_into_memory()

userController = UserController(databaseObject)
adminController = AdminController(databaseObject, catalog_controller)

from application import routes
