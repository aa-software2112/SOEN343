import app.common_definitions.helper_functions as helper_functions
from app.classes.cart import Cart


class User:
    """
        inv:
            self._loan_list.size() <= 10
            allInstances() -> isUnique(id)
            LOAN_LIMIT = 10
    """
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
        self._cart = Cart(self._id)
        self._loan_list = []

    def get_session_dict(self):
        session_dict = {
            "_id": self._id,
            "_first_name": self._first_name,
            "_last_name": self._last_name,
            "_physical_address": self._physical_address,
            "_email": self._email,
            "_phone_number": self._phone_number,
            "_username": self._username,
            "_password": self._password,
            "_is_admin": self._is_admin,
            "_is_logged": self._is_logged,
            "_last_logged": self._last_logged
        }
        return session_dict

    def get_cart_set(self):
        return self._cart.get_set()

    def get_id(self):
        """Returns the id of the object"""
        return self._id

    def add_to_user_cart(self, record_object):
        print(record_object)
        oldsize = (self._cart.length_of_cart())
        self._cart.add_to_cart(record_object)
        newsize = (self._cart.length_of_cart())
        return oldsize, newsize

    def __str__(self):

        return "USER | ID: " + str(
            self._id) + " FIRST_NAME: " + self._first_name + " LAST_NAME: " + self._last_name + " PHYSICAL ADDRESS: " + self._physical_address + \
               " EMAIL: " + self._email + " PHONE_NUMBER: " + str(
            self._phone_number) + " USER_NAME: " + self._username + " PASSWORD: " + self._password + " IS_ADMIN: " + str(
            self._is_admin) + \
               " IS_LOGGED: " + str(self._is_logged) + " LAST_LOGGED: " + str(
            helper_functions.convert_epoch_to_datetime(self._last_logged))

    def get_last_searched_list(self):
        return self._last_searched_list

    def get_index_last_searched(self):
        return self._index_of_last_searched_list

    def set_last_searched_list(self, last_searched_list):
        self._last_searched_list = last_searched_list

    def set_index_last_searched(self, index_last_searched_list):
        self._index_of_last_searched_list = index_last_searched_list

    def get_next_record_searched(self):
        # return next record if list is not empty
        if len(self._last_searched_list) != 0:
            self._index_of_last_searched_list = (self._index_of_last_searched_list + 1) % len(self._last_searched_list)
            return self._last_searched_list[self._index_of_last_searched_list]

    def get_index_from_object(self, object):
        i = 0
        for obj in self._last_searched_list:
            if object._id == obj._id:
                return i
            i = i + 1

    def delete_from_cart(self, o_id, record_type):
        return self._cart.delete_by_id(o_id, record_type)

    def set_loan_list(self, loan_list):
        self._loan_list = loan_list

    def get_loaned_items(self):
        print('returning loaned items list')
        return self._loan_list

    def remove_loan(self, loan_id):
        """
        pre:
            self._loan_list -> size() > 1
            loaned_ids -> size() > 1
            self._loan_list -> collect(id) -> includesAll(loaned_ids)
        post:
            self._loan_list -> forAll( l: Loan ; n: loaned_ids@pre | l.id <> n)

        """
        loan_list_copy = self._loan_list.copy()
        for loan_obj in loan_list_copy:
            if loan_obj.get_id() == int(loan_id):
                self._loan_list.remove(loan_obj)

    def get_username(self):
        return self._username

    def make_loan(self):
        """
        Makes a loan; returns to the front end the successful and unsuccessful commits (record items).
        pre:
            self._cart._cart_items -> size() >= 1
            self._loan_list -> size() < 10
            self._loan_list -> size() + self._cart._cart_items -> size() <= 10

        post:
            self._cart._cart_items -> size() = self._cart._cart_items -> size()@pre - (self._loan_list -> size() - self._loan_list -> size()@pre)
            self._loan_list -> collect(record_id) = self._loan_list@pre -> collect(record_id) +
            self._cart._cart_items@pre -> select(r:Record | not r.is_loaned)
                                     -> collect(record_id)
        """

        if len(self._loan_list) + len(self._cart.get_set()) > User.LOAN_LIMIT:
            return [[], list(self._cart.get_set())]

        commit_results = self._cart.commit_cart()
        loans_to_add = commit_results[0]

        self._loan_list = self._loan_list + loans_to_add

        # return successful/unsuccessful commits (list of records) for displaying on front end
        return commit_results[1:]

    def set_id(self, id):
        """
        Sets the current id of the user in this object, and the cart itself

        :param id:
        :return:
        """

        self._id = id

        self._cart.set_user_owner_id(id)

    def add_to_loan_list(self, loan):
        self._loan_list.append(loan)


class Admin(User):

    def __init__(self, arguments):
        User.__init__(self, arguments)


class Client(User):

    def __init__(self, arguments):
        User.__init__(self, arguments)
