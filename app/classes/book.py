class Book:

    def __init__(self, attributes):
        # Currently from CatalogController, the .fetchall() returns a
        # sqlite3.row object, so I convert it to a dictionary to search the
        # 'id' key
        if 'id' in dict(attributes):
            self._id = attributes['id']
        else:
            self._id = 0
        self._author = attributes['author']
        self._title = attributes['title']
        self._format = attributes['format']
        self._pages = attributes['pages']
        self._publisher = attributes['publisher']
        # Make sure it is in integer format
        self._year_of_publication = int(attributes['year_of_publication'])
        self._language = attributes['language']
        self._ISBN10 = attributes['isbn_10']
        self._ISBN13 = attributes['isbn_13']
        if 'total_quantity' in dict(attributes):
            self._total_quantity = attributes['total_quantity']
        else:
            self._total_quantity = 1
        if 'quantity_available' in dict(attributes):
            self._quantity_available= attributes['quantity_available']
        else:
            self._quantity_available = 1

    def get_id(self):
        """Returns the id of the object"""
        return self._id

    def __str__(self):
        return "Book | ID: " + str(self._id) + " TITLE: " + self._title + " AUTHOR: " + self._author + " FORMAT: " + self._format + " PAGES: " + str(self._pages) + " PUBLISHER: " + self._publisher + " YEAR: " + str(self._year_of_publication) + \
            " LANGUAGE: " + self._language + " ISBN10: " + \
            self._ISBN10 + " ISBN13: " + self._ISBN13 + " TOTAL_QUANTITY: " + str(self._total_quantity) + " QUANTITY_AVAILABLE: " + str(self._quantity_available)
