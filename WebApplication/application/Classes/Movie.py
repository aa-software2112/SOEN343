class Movie:
    def __init__(self, arguments):
        self._id = arguments['id']
        self._title = arguments['title']
        self._director = arguments['director']
        self._producers = arguments['producers']
        self._actors = arguments['actors']
        self._language = arguments['language']
        self._subtitles = arguments['subtitles']
        self._dubbed = arguments['dubbed']
        self._release_date = arguments['release_date']
        self._runtime = arguments['runtime']

    def get_id(self):
        """Returns the id of the object"""
        return self._id

