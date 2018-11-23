from app.common_definitions.helper_functions import convert_epoch_to_datetime as to_datetime


class Album:
    record_type = "Album"
    copy_table_name = "album_copy"

    # Album can be loaned for 2 weeks (converted to seconds, #weeks x days/week x seconds/day)
    loan_time = 2 * 7 * 86400
    
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
        if not (type(arguments['release_date']) == type(" ")):
            # Get the dd/mm/yyyy only
            self._release_date = to_datetime(arguments['release_date']).split(" ")[0]
            
        self._ASIN = arguments['asin']

        if 'total_quantity' in dict(arguments):

            self._total_quantity = arguments["total_quantity"]

        else:

            self._total_quantity = 1

        if 'quantity_available' in dict(arguments):

            self._quantity_available = arguments["quantity_available"]

        else:

            self._quantity_available = 1

        
    def get_id(self):
        """Returns the id of the object"""
        return self._id

    def get_copy_table_name(self):
        return Album.copy_table_name

    def get_title(self):
        return self._title

    def get_type(self):
        return self.record_type

    def get_loan_time(self):
        return Album.loan_time

    def __str__(self):

        return "Album | ID: " + str(self._id) + " TITLE: " + self._title + " ARTIST: " + self._artist + " TYPE: " + self._type + " LABEL: " + self._label + " RELEASE_DATE: " + str(self._release_date) + \
            " ASIN: " + str(self._ASIN) + " TOTAL_QUANTITY: " + str(self._total_quantity) + " QUANTITY_AVAILABLE: " + str(self._quantity_available)

