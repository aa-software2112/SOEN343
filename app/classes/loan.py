import time

class Loan:

    def __init__(self, user_obj, record_obj):
        """
        The loan constructor takes the attributes user user_obj and record_obj
        that are associated with the loan; all values will be set according to those
        passed objects
        :param id
        :param user_obj: The user making the loan (as an object)
        :param record_obj: The record being loaned (as an object)
        """
        # The loan times are added here manually,

        self.id = -1

        self._user_id = user_obj.get_id()

        self._record_id = record_obj.get_id()

        self._table_name = record_obj.get_copy_table_name()

        self._loan_time = time.time()

        self._due_time = self._loan_time + record_obj.get_loan_time()

        # maintains a reference to the object reserved, and the user that holds it
        self._record = record_obj

        self._user = user_obj

        # Object has not yet been returned, no return time assigned yet
        self._return_time = -1

        # Object has not yet been returned, this evaluated to zero
        self._is_returned = 0

    def set_loan_as_returned(self):
        """
        This function sets the return time, along with the
        status of "is returned". In addition, the loan should be
        dissociated from the records it currently points to
        :return: N/A
        """

        self._return_time = time.time()

        self._is_returned = 1

        self._record = None

        self._user = None

    def set_loan_id(self, id):
        """
        Sets the loan id; initially starts off as -1, must be set after
        adding it to the database
        :param id: The id for this loan
        :return: N/A
        """
        self._id = id

    def get_id(self):
        """
        Returns the id of the loan
        :return: id
        """
        return self._id


    def __str__(self):
        return "Loan | ID: " + str(self._id) + "UserID: " + self._user_id + "RecordID: " + self._record_id + "Table Name: " + self._table_name \
                + "Loan Time: " + self._loan_time + "Due Time: "+ self._due_time + "Return Time: "+ self._return_time + "Is Returned: " + self._is_returned