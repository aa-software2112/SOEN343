class Book:
    def __init__(self, attributes):
        self._id = attributes['id']
        self._author = attributes['author']
        self._title = attributes['title']
        self._format = attributes['format']
        self._pages = attributes['pages']
        self._publisher = attributes['publisher']
        self._year_of_publication = attributes['year_of_publication']
        self._language = attributes['language']
        self._ISBN10 = attributes['ISBN10']
        self._ISBN13 = attributes['ISBN13']

    def get_id(self):
        """Returns the id of the object"""
        return self._id
