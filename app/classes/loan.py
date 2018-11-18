class Loan:

    def __init__(self, attributes):
        if 'id' in dict(attributes):
            self._id = attributes['id']
        else:
            self._id = 0
        self._user_id = attributes['user_id']
        self._record_id = attributes['record_id']
        self._table_name = attributes['table_name']
        self._loan_time = attributes['loan_time']
        self._due_time = attributes['due_time']
        self._return_time = attributes['return_time']
        self._is_returned = attributes['is_returned']

    def __str__(self):
        return "Loan | ID: " + str(self._id) + "UserID: " + self._user_id + "RecordID: " + self._record_id + "Table Name: " + self._table_name \
                + "Loan Time: " + self._loan_time + "Due Time: "+ self._due_time + "Return Time: "+ self._return_time + "Is Returned: " + self._is_returned