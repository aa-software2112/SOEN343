"""
This module contains general helper functions.
"""
from functools import wraps
from flask import g, redirect, request, url_for, flash
import time
import datetime


def convert_epoch_to_datetime(epoch_time):
    """Returns time in 'month/day/year hour:minute:second' format given the epoch time"""
    return time.strftime("%m/%d/%Y %H:%M:%S %Z", time.localtime(epoch_time))

def convert_date_time_to_epoch(date_time_string):
    """ Expects a string in the form mm/dd/yyyy, otherwise returns
    current epoch time"""
    date_time_string = date_time_string.split("/")
    print(date_time_string)
    if( not(len(date_time_string) == 3)):
        return time.time()
        
    return datetime.datetime(int(date_time_string[2]), int(date_time_string[0]), int(date_time_string[1]), 0, 0, 0, 0).timestamp()


def login_required(f):
    @wraps(f)
    # if the user isn't logged in, redirect to the login page
    def login_check(*args, **kwargs):
        if g.user is None:
            flash('Please login first!', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return login_check


def is_logged(f):
    @wraps(f)
    def login_check(*args, **kwargs):
        if g.user:
            flash('You are already logged in', 'warning')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return login_check


def admin_required(f):
    @wraps(f)
    def admin_check(*args, **kwargs):
        # if the user isn't an admin, redirect to the home page, else the
        # function has access to g.user
        if g.user["_is_admin"]:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized Access!', 'danger')
            return redirect(url_for('index'))
    return admin_check


def search_catalog(catalog, search_string):
    """ Performs a search on the catalog and returns a list of all the catalog 
    items which contain the string inside their title (case insensitive)"""

    lst = []

    for k, v in catalog.items():
        title = str(v.__dict__['_title'])
        title_lower = title.lower()

        if search_string in title_lower:
            print("Match found! Title: " + title)
            lst.append(v)

    return lst