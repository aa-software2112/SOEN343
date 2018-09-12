from application.automationFiles.generateRoutesDotPy import generateRoutesFile as genRoutePy 

# Generates the routes.py file
genRoutePy()

# Sets up the application for running
from flask import Flask
import random

app = Flask(__name__)

# Imports the routes file
from application import routes
