import os
from flask import Flask

app = Flask(__name__)

from app.classes.database_container import DatabaseContainer
from app.common_definitions.common_paths import PATH_TO_DATABASE
from app.database import sqlite_script
from app.controllers.client_controller import ClientController
from app.controllers.admin_controller import AdminController
from app.controllers.catalog_controller import CatalogController
from app.common_definitions import helper_functions

# Creates a database as an abstracted object - this object must be imported into route files for use
databaseObject = DatabaseContainer(PATH_TO_DATABASE)

# Send the database object to all Controllers
catalog_controller = CatalogController(databaseObject)
client_controller = ClientController(databaseObject, catalog_controller)
admin_controller = AdminController(databaseObject, catalog_controller)

# Create and fill database with values - closses connecton to database when its done
sqlite_script.initializeAndFillDatabase(databaseObject, catalog_controller, client_controller,admin_controller)

#Makes a new connection to database for the application to use after tables are filled
databaseObject.make_connection()

#load database to memory
catalog_controller.load_database_into_memory()
client_controller.load_database_into_memory()
admin_controller.load_database_into_memory()

# Helper function to be used in front end
app.jinja_env.globals.update(convert_epoch_to_datetime=helper_functions.convert_epoch_to_datetime)

from app import routes