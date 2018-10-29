class Album:

    def __init__(self, arguments):
        # Currently from CatalogController, the .fetchall() returns a
        # sqlite3.row object, so I convert it to a dictionary to search the
        # 'id' key
        if 'id' in dict(arguments):
            self._id = arguments['id']
        else:
            self._id = 0
        self._type = arguments['type']
        self._title = arguments['title']
        self._artist = arguments['artist']
        self._label = arguments['label']
        self._release_date = arguments['release_date']
        self._ASIN = arguments['asin']

    def get_id(self):
        """Returns the id of the object"""
        return self._id

    def __str__(self):

        return "Album | ID: " + str(self._id) + " TITLE: " + self._title + " ARTIST: " + self._artist + " TYPE: " + self._type + " LABEL: " + self._label + " RELEASE_DATE: " + self._release_date + \
            " ASIN: " + self._ASIN
