class Book:
    def __init__(self, attributes):
        self._id = attributes['id']
        self._author = attributes['author']
        self._title = attributes['title']
        # self._format = attributes['format']
        # self._pages = attributes['pages']
        # self._publisher = attributes['publisher']
        # self._yearOfPublication = attributes['yearOfPublication']
        # self._language = attributes['language']
        # self._ISBN10 = attributes['ISBN10']
        # self._ISBN13 = attributes['ISBN13']
    def getId(self):
        return self._id