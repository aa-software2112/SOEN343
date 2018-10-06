class Movie:
    def __init__(self, arguments):
        self._id = arguments['id']
        self._title = arguments['title']
        self._director = arguments['director']
        self._producers = arguments['producers']
        self._actors = arguments['actors']
        self._language = arguments['language']
        self._subtitles =arguments['subtitles']
        self._dubbed = arguments['dubbed']
        self._releaseDate = arguments['releaseDate']
        self._runtime = arguments['runTime']
    def getId(self):
        return self._id

