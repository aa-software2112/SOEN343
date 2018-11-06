import app.common_definitions.helper_functions as helper_functions

class User:

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

    def get_id(self):
        """Returns the id of the object"""
        return self._id

    def __str__(self):

        return "USER | ID: " + str(self._id) + " FIRST_NAME: " + self._first_name + " LAST_NAME: " + self._last_name + " PHYSICAL ADDRESS: " + self._physical_address +\
               " EMAIL: " + self._email + " PHONE_NUMBER: " + str(self._phone_number) + " USER_NAME: " + self._username + " PASSWORD: " + self._password + " IS_ADMIN: " + str(self._is_admin) + \
            " IS_LOGGED: " + str(self._is_logged) + " LAST_LOGGED: " + str(helper_functions.convert_epoch_to_datetime(self._last_logged))

class Admin(User):

    def __init__(self, arguments):
        User.__init__(self, arguments)

class Client(User):

    def __init__(self, arguments):
        User.__init__(self, arguments)


import time

l = []

d = {'id': 1, 'firstName':"Anthony",
     "lastName":"Andreoli",
     "physicalAddress":"7331",
     "email":"a@a",
     "phoneNumber":"555",
     "username":"AA",
     "password":"pw",
     "isAdmin":1,
     "isLogged":1,
     "lastLogged":time.time()}


for i in range(10):

    l.append(User(d))
    print(l[0].__dict__["_physical_address"])

