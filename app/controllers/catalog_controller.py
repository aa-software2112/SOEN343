from app.controllers.controller import Controller
from app.classes.album import Album
from app.classes.book import Book
from app.classes.magazine import Magazine
from app.classes.movie import Movie
from app.classes.loan import Loan
from app.classes.catalogs import Catalog
from app.classes.catalogs import LoanCatalog, AlbumCatalog, MovieCatalog, BookCatalog, MagazineCatalog
from app.classes.database_container import DatabaseContainer

class CatalogController(Controller):
    """
    This class uses the Singleton pattern.
    """
    _instance = None

    BOOK_TYPE = "1"
    MOVIE_TYPE = "2"
    MAGAZINE_TYPE = "3"
    ALBUM_TYPE = "4"
    #LOAN_TYPE = "5"

    @staticmethod
    def get_instance():
        """ Static access method. """
        if CatalogController._instance is None:
            CatalogController._instance = CatalogController()
        return CatalogController._instance

    def __init__(self):
        if CatalogController._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            CatalogController._instance = self
            Controller.__init__(self, DatabaseContainer.get_instance())
            self._inventory = {CatalogController.BOOK_TYPE: BookCatalog.get_instance(),
                               CatalogController.MOVIE_TYPE: MovieCatalog.get_instance(),
                               CatalogController.MAGAZINE_TYPE: MagazineCatalog.get_instance(),
                               CatalogController.ALBUM_TYPE: AlbumCatalog.get_instance(),
                               #CatalogController.LOAN_TYPE: LoanCatalog.get_instance()}
            self._constructors = {CatalogController.BOOK_TYPE: Book,
                                  CatalogController.MOVIE_TYPE: Movie,
                                  CatalogController.MAGAZINE_TYPE: Magazine,
                                  CatalogController.ALBUM_TYPE: Album,
                                  #CatalogController.LOAN_TYPE: Loan}
            self._db_loaded = False

    def load_database_into_memory(self):

        # Database cannot be loaded into memory more than once
        if not self._db_loaded:
            self._db_loaded = True
        else:
            raise Exception("Cannot load db into memory more than once!")

        # Add all objects form database into catalogs
        queries = {CatalogController.BOOK_TYPE: """ SELECT * FROM book; """,
                   CatalogController.MOVIE_TYPE: """ SELECT * FROM movie; """,
                   CatalogController.MAGAZINE_TYPE: """ SELECT * FROM magazine; """,
                   CatalogController.ALBUM_TYPE: """ SELECT * FROM album; """,
                   #CatalogController.LOAN_TYPE: """ SELECT * FROM loan; """
                   }

        # Iterate over all queries
        for catalog_type, query in queries.items():

            all_rows = self.db.execute_query(query).fetchall()

            catalog = self._inventory[catalog_type]

            constructor = self._constructors[catalog_type]

            # Create an object for each row
            for row in all_rows:
                catalog.add(constructor(row), False)

        # Uncomment these two lines to see all objects in all catalogs
        # for k, v in self._inventory.items():
        #    v.display()

    def get_all_catalogs(self):

        dict_of_catalogs = {"books": self._inventory[CatalogController.BOOK_TYPE].get_all(),
                            "movies": self._inventory[CatalogController.MOVIE_TYPE].get_all(),
                            "magazines": self._inventory[CatalogController.MAGAZINE_TYPE].get_all(),
                            "albums": self._inventory[CatalogController.ALBUM_TYPE].get_all(),
                            "loan": self._inventory[CatalogController.LOAN_TYPE].get_all()
                            }
        return dict_of_catalogs

    def get_records_by_catalog(self, catalog_type):
        return self._inventory[catalog_type].get_all()

    def get_constructor(self, catalog_type):
        return self._constructors[catalog_type]

    def add_entry_to_catalog(self, catalog_type, record_key_values):

        print(catalog_type)
        print(record_key_values)

        # Create the new record based on catalog_type and key_values
        new_record = self.get_constructor(catalog_type)(record_key_values)

        # Add the object to the catalog
        self._inventory[catalog_type].add(new_record, True)

    def view_catalog_inventory(self):
        return self._inventory

    def modify_catalog_entry(self, type, modified_entry_object):
        return self._inventory[type].modify(modified_entry_object)

    def get_catalog_entry_by_id(self, catalog_type, id):

        return self.view_catalog_inventory()[catalog_type].get(id)

    def get_catalog_entry_copies_by_id(self, catalog_type, id):
        return self.view_catalog_inventory()[catalog_type].get_copies(id)

    def delete_catalog_entry_copy(self, catalog_type, id):
        self.view_catalog_inventory()[catalog_type].remove_copy(id)

    def get_filters(self, catalog_type):
        return sorted(list(self.view_catalog_inventory()[catalog_type].Filters.keys()))

    def get_sorting_criteria(self, catalog_type):
        return sorted(list(self.view_catalog_inventory()[catalog_type].Sorts.keys()))

    def sort_by(self, catalog_type, sort_key_values, last_searched_list):

        # No sorting criteria was provided, return the list as-is
        if sort_key_values.strip() == "":
            return last_searched_list

        return self.view_catalog_inventory()[catalog_type].sort(sort_key_values, last_searched_list)

    def filter_by(self, catalog_type, filter_key_values, last_searched_list):

        # Remove the keys with no value
        transformed_filter_key_values = {}

        for k, v in filter_key_values.items():

            # Empty key, don't use this as a filter
            if not v.strip() == "":
                transformed_filter_key_values[k] = v

        if len(transformed_filter_key_values) == 0:
            return last_searched_list

        return self.view_catalog_inventory()[catalog_type].filter(transformed_filter_key_values, last_searched_list)

    def search_from(self, catalog_type, search_value):
        return self.view_catalog_inventory()[catalog_type].search(search_value)

    '''
    def search_transaction_by(self, search_transaction_key_values):

        # Remove the keys with no value
        transformed_search_transaction_key_values = {}
        
        for k, v in search_transaction_key_values.items():

            # Empty key, don't use this as a search_transaction
            if not v.strip() == "":
                transformed_search_transaction_key_values[k] = v

        empty_list = []

        if len(transformed_search_transaction_key_values) == 0:
            return empty_list
        
        lst = self.view_catalog_inventory()["5"].search_transaction(transformed_search_transaction_key_values)
        
        return lst

    def view_transaction_history(self):
        loan_catalog = self.view_catalog_inventory()["5"]
        lst = []
        for k, v in loan_catalog.items():
            lst.append(v)

        return lst
    '''