class Book:
    record_type = "Book"
    copy_table_name = "book_copy"

    # Book can be loaned for 1 week (converted to seconds, #weeks x days/week x seconds/day)
    loan_time = 1 * 7 * 86400

    def __init__(self, arguments):
        # Currently from CatalogController, the .fetchall() returns a
        # sqlite3.row object, so I convert it to a dictionary to search the
        # 'id' key
        if 'id' in dict(arguments):
            self._id = arguments['id']
        else:
            self._id = 0
        self._author = arguments['author']
        self._title = arguments['title']
        self._format = arguments['format']
        self._pages = arguments['pages']
        self._publisher = arguments['publisher']
        # Make sure it is in integer format

        self._year_of_publication = int(arguments['year_of_publication'])
        self._language = arguments['language']
        self._ISBN10 = arguments['isbn_10']
        self._ISBN13 = arguments['isbn_13']

        if 'total_quantity' in dict(arguments):

            self._total_quantity = arguments["total_quantity"]

        else:

            self._total_quantity = 1

        if 'quantity_available' in dict(arguments):

            self._quantity_available = arguments["quantity_available"]

        else:

            self._quantity_available = 1

    def get_id(self):
        """Returns the id of the object"""
        return self._id

    def get_copy_table_name(self):
        return Book.copy_table_name

    def get_title(self):
        return self._title

    def get_type(self):
        return self.record_type

    def get_loan_time(self):
        return Book.loan_time

    def __str__(self):
        return "Book | ID: " + str(self._id) + " TITLE: " + self._title + " AUTHOR: " + self._author + " FORMAT: " + self._format + " PAGES: " + str(self._pages) + " PUBLISHER: " + self._publisher + " YEAR: " + str(self._year_of_publication) + \
            " LANGUAGE: " + self._language + " ISBN10: " + \
            self._ISBN10 + " ISBN13: " + self._ISBN13 + " TOTAL_QUANTITY: " + str(self._total_quantity) + " QUANTITY_AVAILABLE: " + str(self._quantity_available)
