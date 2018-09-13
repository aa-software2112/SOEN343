from flask import render_template
from application import app
import random

# All routes from route folder are imported here...
from application.routesToPages import routeToDBDeleteRecord
from application.routesToPages import routeToIndex
from application.routesToPages import routeToDBQuerryRecord
from application.routesToPages import routeToLogin
from application.routesToPages import routeToExample
from application.routesToPages import routeToDBInsertRecord
