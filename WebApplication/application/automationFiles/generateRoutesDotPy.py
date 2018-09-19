import glob, os

""" Generates the routes.py file located in WebApplication/application/routes.py;
It is run right before the server is initialized, so any routes added to WebApplication/application/routesToPages/ 
with the name routeTo<PageName>.py will automatically be linked to the website
"""
def generateRoutesFile():
	# Store the current working directory
	previousPath = os.getcwd()

	# Move directory to this file's location - assumes generateRoutesDotPy was executed from somewhere in /WebApplication/...
	os.chdir(os.getcwd().split("WebApplication")[0] + "WebApplication/application/RoutesToPages")

	# File System Definitions
	PATH_TO_ROUTES_DOT_PY = "../routes.py"
	ROUTES_TO_PAGES_DIR = "RoutesToPages"
	PATH_TO_ROUTES_TO_PAGES_DIRECTORY = "../" + ROUTES_TO_PAGES_DIR
	ROUTE_FILENAME_PREFIX = "routeTo"
	APPLICATION_PACKAGE_NAME = "application"

	# routes.py import string
	routesImportString = "from flask import render_template\nfrom application import app\nimport random\n\n# All routes from route folder are imported here...\n"

	# Get all the route filenames 
	routes = [os.path.basename(filePath).replace(".py","") for filePath in glob.glob(PATH_TO_ROUTES_TO_PAGES_DIRECTORY + "/" + ROUTE_FILENAME_PREFIX + "*.py")]

	# Open routes.py and write a fresh implementation based on current filesystem
	routesDotPyFileHandle = open(PATH_TO_ROUTES_DOT_PY, 'w')

	# Write import string
	routesDotPyFileHandle.write(routesImportString)

	# Write all routes to routes.py
	for route in routes:
		routesDotPyFileHandle.write("from {}.{} import {}\n".format(APPLICATION_PACKAGE_NAME, ROUTES_TO_PAGES_DIR, route))
		print ("Added {} to {}".format(route, "routes.py"))

	# Close handle
	routesDotPyFileHandle.close()

	# Revert working directory back to initial state
	os.chdir(previousPath)
