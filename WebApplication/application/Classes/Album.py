class Album:
    def __init__(self,arguments):
        self._id = arguments['id']
        self._type = arguments['type']
        self._title = arguments['title']
        self._artist = arguments['artist']
        self._label = arguments['label']
        self._release_date = arguments['release_date']
        self._ASIN = arguments['ASIN']

    def get_id(self):
        """Returns the id of the object"""
        return self._id
