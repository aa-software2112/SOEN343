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

    def add_book_to_catalog(self, book):
        self._inventory[CatalogController.BOOK_TYPE].add(book, True)

    def add_movie_to_catalog(self, movie):
        self._inventory[CatalogController.MOVIE_TYPE].add(movie, True)

    def add_magazine_to_catalog(self, magazine):
        self._inventory[CatalogController.MAGAZINE_TYPE].add(magazine, True)

    def add_album_to_catalog(self, album):
        self._inventory[CatalogController.ALBUM_TYPE].add(album, True)

    def view_catalog_inventory(self):
        return self._inventory

    def get_book_by_id(self, id):
        return self.get_all_catalogs()['books'].get(id)

    def get_magazine_by_id(self, id):
        return self.get_all_catalogs()['magazines'].get(id)

    def get_album_by_id(self, id):
        return self.get_all_catalogs()['albums'].get(id)

    def get_movie_by_id(self, id):
        return self.get_all_catalogs()['movies'].get(id)