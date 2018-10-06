class Magazine:
    def __init__(self,arguments):
        self._id = arguments['id']
        self._title = arguments['title']
        self._publisher = arguments['publisher']
        self._year_of_publication = arguments['year_of_publication']
        self._language = arguments['language']
        self._ISBN10 = arguments['ISBN10']
        self._ISBN13 = arguments['ISBN13']

    def get_id(self):
        """Returns the id of the object"""
        return self._id
