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



#Assuming sortKeyValues = holds criteria dictionnary of ascending/descenting, Attribute. Ex: {"ascending": "Title"}
#Assuming lastSearchedList = holds id of object book and row of 1 object book as list.
def sort_book(sortKeyValues, lastSearchedList)

    #gets the order to which it will be sorted (ascending or descending) from the sortKeyValues criteria
    sort_order =  list(sortKeyValues.keys())[0]

    #Gives the attributes to sort the book objects to. Taken from the sortKeyValues criteria
    sort_attribute = list(sortKeyValue.values())[0]

    #Holds boolean which will be used to sort inorder or in reverse order
    if sort_order = "ascending"
        reverse_order = False
    else if sort_order = "descending"
        reverse_order = True
    else 
        print("criteria value isn't properly defined in terms of ascending or descending")
        reverse_order = None
        return reverse_order

    #Sorts the catalogs items by its value in reverse order or in order.
    #Note: since python3 doesn't allow unpacking: https://www.python.org/dev/peps/pep-3113/
    #An example: https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary
    list_sorted = sorted(lastSearchedList.items(), key=lambda kv: kv[sort_attribute], reverse=reverse_order)

    return list_sorted















       




