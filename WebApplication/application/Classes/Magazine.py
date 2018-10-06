class Magazine:
    def __init__(self,arguments):
        self._id = arguments['id']
        self._title = arguments['title']
        self._publisher = arguments['publisher']
        self._yearOfPublication = arguments['yearOfPublication']
        self._language = arguments['language']
        self._ISBN10 = arguments['ISBN10']
        self._ISBN13 = arguments['ISBN13']
    def getId(self):
        return self._id
