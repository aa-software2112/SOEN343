from app.common_definitions.helper_functions import convert_epoch_to_datetime as to_datetime


class Movie:
    # Movie can be loaned for 2 weeks (converted to seconds, #weeks x days/week x seconds/day)
    loan_time = 2 * 7 * 86400

    def __init__(self, arguments):
        # Currently from CatalogController, the .fetchall() returns a
        # sqlite3.row object, so I convert it to a dictionary to search the
        # 'id' key
        if 'id' in dict(arguments):
            self._id = arguments['id']
        else:
            self._id = 0
        self._title = arguments['title']
        self._director = arguments['director']
        self._producers = arguments['producers']
        self._actors = arguments['actors']
        self._language = arguments['language']
        self._subtitles = arguments['subtitles']
        self._dubbed = arguments['dubbed']
        self._release_date = arguments['release_date']
        # If the passed release date is a string (datetime format), do nothing
        if not (type(arguments['release_date']) == type(" ")):
            # Get the dd/mm/yyyy only
            self._release_date = to_datetime(arguments['release_date']).split(" ")[0]
        self._runtime = arguments['run_time']
        self._total_quantity = 1
        self._quantity_available = 1

    def get_id(self):
        """Returns the id of the object"""
        return self._id

    def __str__(self):

        return "Movie | ID: " + str(self._id) + " TITLE: " + self._title +  " DIRECTOR: " + self._director + " PRODUCERS: " + self._producers + " ACTORS: " + self._actors + \
            " LANGUAGE: " + self._language + " SUBTITLES: " + self._subtitles + " DUBBED: " + \
            self._dubbed + " RELEASE_DATE: " + self._release_date + \
            " RUNTIME: " + str(self._runtime) + " TOTAL_QUANTITY: " + str(self._total_quantity) + " QUANTITY_AVAILABLE: " + str(self._quantity_available)
