import app.common_definitions.helper_functions as helper_functions
from app.classes.cart import Cart

class User:
    #Maximun number of items that can be loaned by a single user
    LOAN_LIMIT = 10

    def __init__(self, arguments):

        if 'id' in dict(arguments):
            self._id = arguments['id']
        else:
            self._id = 0
        self._first_name = arguments['firstName']
        self._last_name = arguments['lastName']
        self._physical_address = arguments['physicalAddress']
        self._email = arguments['email']
        self._phone_number = arguments['phoneNumber']
        self._username = arguments['username']
        self._password = arguments['password']
        self._is_admin = arguments['isAdmin']
        self._is_logged = arguments['isLogged']
        self._last_logged = arguments['lastLogged']
        
        self._last_searched_list = []
        self._index_of_last_searched_list = 0
        self._cart = Cart()
        self._loan_list = []

    def get_cart_set(self):
        return self._cart.get_set()

    def get_id(self):
        """Returns the id of the object"""
        return self._id

    def __str__(self):

        return "USER | ID: " + str(self._id) + " FIRST_NAME: " + self._first_name + " LAST_NAME: " + self._last_name + " PHYSICAL ADDRESS: " + self._physical_address +\
               " EMAIL: " + self._email + " PHONE_NUMBER: " + str(self._phone_number) + " USER_NAME: " + self._username + " PASSWORD: " + self._password + " IS_ADMIN: " + str(self._is_admin) + \
            " IS_LOGGED: " + str(self._is_logged) + " LAST_LOGGED: " + str(helper_functions.convert_epoch_to_datetime(self._last_logged))

    def get_last_searched_list(self):
        return self._last_searched_list

    def get_index_last_searched(self):
        return self._index_of_last_searched_list

    def set_last_searched_list(self, last_searched_list):
        self._last_searched_list=last_searched_list

    def set_index_last_searched(self, index_last_searched_list):
        self._index_of_last_searched_list=index_last_searched_list

    def get_next_record_searched(self):
        # return next record if list is not empty
        if len(self._last_searched_list)!=0 :
            self._index_of_last_searched_list = (self._index_of_last_searched_list +1)%len(self._last_searched_list)
            return self._last_searched_list[self._index_of_last_searched_list]

    def get_index_from_object(self, object):
        i = 0
        for obj in self._last_searched_list:
            if object._id == obj._id:
                return i
            i = i+1


        
class Admin(User):

    def __init__(self, arguments):
        User.__init__(self, arguments)


class Client(User):

    def __init__(self, arguments):
        User.__init__(self, arguments)
    