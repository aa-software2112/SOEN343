from application.automationFiles.generateRoutesDotPy import generateRoutesFile as genRoutePy 

# Generates the routes.py file
genRoutePy()

# Sets up the application for running
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Imports the routes file
from application import routes, models
