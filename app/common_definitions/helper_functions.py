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

  
#Sorts a list of dictionnary (i.e. lastSearchedList) based on criteria provided (i.e sorKeyValues)
#sortKeyValues = holds criteria dictionnary of ascending/descenting, Attribute. Ex: {"ascending": "Title"}
#lastSearchedList = holds list of objects dictionnary
def sort_book(sortKeyValues, lastSearchedList):

    print("Unsorted list")
    print(lastSearchedList)

    #gets the order to which it will be sorted (ascending or descending) from the sortKeyValues criteria
    sort_order =  list(sortKeyValues.keys())[0]

    #Gives the attributes to sort the book objects to. Taken from the sortKeyValues criteria
    sort_attribute = list(sortKeyValues.values())[0]

    #Holds boolean which will be used to sort inorder or in reverse order   
    if sort_order is "ascending":
        reverse_order = False
    elif sort_order is "descending":
        reverse_order = True
    else: 
        print("criteria value isn't properly defined in terms of ascending or descending")
        reverse_order = None
        return reverse_order

    #Sorts the catalogs items by its value in reverse order or in order.
    #Note: since python3 doesn't allow unpacking: https://www.python.org/dev/peps/pep-3113/
    #An example: https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary
    last_searched_list_sorted = sorted(lastSearchedList, key=lambda kv: kv[sort_attribute], reverse=reverse_order)

    print("Sorted list")
    print(last_searched_list_sorted)
    return last_searched_list_sorted

#4 lines below For testing sort_book, can be removed after review. To test, remove number sign to uncomment it.
#sortKeyValues1 = {"descending": "author"}
#lastSearchedList1 = [{"title": 6, "author": "c", "type": "Hardcover"}, {"title": 3, "author": "f", "type": "Digital"}, {"title": 9, "author": "a", "type": "Paperback"},]
#rint("testing sort_book")
#sort_book(sortKeyValues1, lastSearchedList1)



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
