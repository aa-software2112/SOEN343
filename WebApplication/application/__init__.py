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
 4. Creating the database object that will contain ALL manipulators
 Imports the routes file

 """
from application.Classes.DatabaseContainer import DatabaseContainer
from application.CommonDefinitions.CommonPaths import PATH_TO_DATABASE
from application.Database.SQLiteScript import initializeAndFillDatabase

# Create and fill database with values - closes connection to 
initializeAndFillDatabase(PATH_TO_DATABASE)

# Connect to the database through an abstracted object
databaseObject = DatabaseContainer(PATH_TO_DATABASE)

from application import routes
