"""
This file includes all paths and filenames common across entire application
"""
from os import getcwd

DATABASE_NAME = "SOEN343_DATABASE.db"
PATH_TO_DATABASE = getcwd().split("WebApplication")[0] + "WebApplication/application/Database/" + DATABASE_NAME

