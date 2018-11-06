from app.controllers.controller import Controller
from app.classes.album import Album
from app.classes.book import Book
from app.classes.magazine import Magazine
from app.classes.movie import Movie
from app.classes.catalogs import *


class CatalogController(Controller):
    BOOK_TYPE = "1"
    MOVIE_TYPE = "2"
    MAGAZINE_TYPE = "3"
    ALBUM_TYPE = "4"

    def __init__(self, database):
        Controller.__init__(self, database)
        self._inventory = {CatalogController.BOOK_TYPE: BookCatalog(database),
                           CatalogController.MOVIE_TYPE: MovieCatalog(database),
                           CatalogController.MAGAZINE_TYPE: MagazineCatalog(database),
                           CatalogController.ALBUM_TYPE: AlbumCatalog(database)}
        self._constructors = {CatalogController.BOOK_TYPE: Book,
                              CatalogController.MOVIE_TYPE: Movie,
                              CatalogController.MAGAZINE_TYPE: Magazine,
                              CatalogController.ALBUM_TYPE: Album}
        self._db_loaded = False

    def load_database_into_memory(self):

        # Database cannot be loaded into RAM more than once
        if not (self._db_loaded):
            self._db_loaded = True

        # Add all objects form database into catalogs
        queries = {CatalogController.BOOK_TYPE: """ SELECT * FROM book; """,
                   CatalogController.MOVIE_TYPE: """ SELECT * FROM movie; """,
                   CatalogController.MAGAZINE_TYPE: """ SELECT * FROM magazine; """,
                   CatalogController.ALBUM_TYPE: """ SELECT * FROM album; """
                   }

        # Iterate over all queries
        for catalog_type, query in queries.items():

            all_rows = self.db.execute_query(query).fetchall()

            catalog = self._inventory[catalog_type]

            constructor = self._constructors[catalog_type]

            # Create an object for each row
            for row in all_rows:
                #	print(type(constructor(row)._id))
                catalog.add(constructor(row), False)

        # Uncomment these two lines to see all objects in all catalogs
        #for k, v in self._inventory.items():
        #    v.display()

    def get_all_catalogs(self):

        dict_of_catalogs = {"books": self._inventory[CatalogController.BOOK_TYPE].get_all(),
                            "movies": self._inventory[CatalogController.MOVIE_TYPE].get_all(),
                            "magazines": self._inventory[CatalogController.MAGAZINE_TYPE].get_all(),
                            "albums": self._inventory[CatalogController.ALBUM_TYPE].get_all()
                            }
        return dict_of_catalogs

    def add_entry_to_catalog(self, type, new_record_object):
        self._inventory[type].add(new_record_object, True)

    def view_catalog_inventory(self):
        return self._inventory

    def modify_catalog_entry(self, type, modified_entry_object):
        return self._inventory[type].modify(modified_entry_object)

    def get_catalog_entry_by_id(self,catalog_type, id):
        return self.view_catalog_inventory()[catalog_type].get(id)

    def get_catalog_entry_copies_by_id(self, catalog_type, id):
        return self.view_catalog_inventory()[catalog_type].get_copies(id)

    def delete_catalog_entry_copy(self, catalog_type, id):
        self.view_catalog_inventory()[catalog_type].remove_copy(id)

    def get_filters(self, catalog_type):
        return sorted(list(self.view_catalog_inventory()[catalog_type].Filters.keys()))

    def search_from(self, catalog_type, search_value):
        return self.view_catalog_inventory()[catalog_type].search(search_value)
