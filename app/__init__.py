import os
import sys
from flask import Flask

app = Flask(__name__)

from app.classes.database_container import DatabaseContainer
from app.common_definitions.common_paths import PATH_TO_DATABASE
from app.database import sqlite_script
from app.controllers.client_controller import ClientController
from app.controllers.admin_controller import AdminController
from app.controllers.catalog_controller import CatalogController
from app.common_definitions import helper_functions

# Create and fill database with values - closes connection to
# Database was filled, objects are in memory if function call returns True
objects_in_memory = sqlite_script.initializeAndFillDatabase()


# Connect to the database through an abstracted object - this object must be imported into route files for use
databaseObject = DatabaseContainer.get_instance()

# Send the database object to all Controllers
catalog_controller = CatalogController.get_instance()

client_controller = ClientController.get_instance()

admin_controller = AdminController.get_instance()

if not objects_in_memory:
    catalog_controller.load_database_into_memory()
    client_controller.load_database_into_memory()
    admin_controller.load_database_into_memory()

# Helper function to be used in front end
app.jinja_env.globals.update(convert_epoch_to_datetime=helper_functions.convert_epoch_to_datetime)

from app import routes