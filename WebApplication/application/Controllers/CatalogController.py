from application.Controllers.Controller import Controller
from application.Classes.Album import Album
from application.Classes.Book import Book
from application.Classes.Magazine import Magazine
from application.Classes.Movie import Movie
from application.Classes.Catalogs import * 

class CatalogController(Controller):

	BOOK_TYPE = "1"
	MOVIE_TYPE = "2"
	MAGAZINE_TYPE = "3"
	ALBUM_TYPE = "4"

	def __init__(self, database):
		Controller.__init__(self, database)
		self._inventory = {CatalogController.BOOK_TYPE: BookCatalog(),
							CatalogController.MOVIE_TYPE: MovieCatalog(),
							CatalogController.MAGAZINE_TYPE: MagazineCatalog(),
							CatalogController.ALBUM_TYPE: AlbumCatalog()}
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
				
				all_rows = self.db.executeQuery(query).fetchall()
				
				catalog = self._inventory[catalog_type]
			
				constructor = self._constructors[catalog_type]
				
				# Create an object for each row
				for row in all_rows:
					catalog.add(constructor(row))
			
			# Uncomment these two lines to see all objects in all catalogs
			for k, v in self._inventory.items():
				v.display()
					
			
	
	def viewInventory(self):
		return self._inventory


