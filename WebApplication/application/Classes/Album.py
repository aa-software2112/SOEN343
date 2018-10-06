class Album:
    def __init__(self,arguments):
        self._id = arguments['id']
        self._type = arguments['type']
        self._title = arguments['title']
        self._artist = arguments['artist']
        self._label = arguments['label']
        self._releaseDate = arguments['releaseDate']
        self._ASIN = arguments['ASIN']
    def getId(self):
        return self._id
