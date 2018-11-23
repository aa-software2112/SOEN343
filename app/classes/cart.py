import app.classes.catalogs

class Cart:
	"""
	inv:
		self._items -> isUnique(id)
	"""
	def __init__(self, client_id):
		self._items = set()
		self._client_id = client_id
		self._loan_catalog = app.classes.catalogs.LoanCatalog.get_instance()

	def set_user_owner_id(self, id):
		self._client_id = id

	def get_set(self):
		return self._items

	def add_to_cart(self, item):
		self._items.add(item)
	def length_of_cart(self):
		return self._items.__len__()

	def delete_by_id(self, id, item_type):
		print(item_type)
		for item in self._items:
			if (item.get_id() == id) and (item.record_type == item_type):
				self._items.discard(item)
				return "Item successfully removed from cart"

		return "Item could not be found in cart"

	def commit_cart(self):
		"""
		This function attempts to commit every cart item; and will return three lists:
		loans: a list of the loans that were (successfully) made.
		successful_commits: a list of the cart items that were committed successfully.
		failed_commits: a list of the cart items that were committed unsuccessfully.

		pre:
			self._items -> size() > 0
		post:
			self._items -> size()  <= self._items -> size()@pre
		"""
		loans = []
		successful_commits = []
		failed_commits = []
		print("self in commit_Cart")
		print(self._loan_catalog)
		for item in self._items:
			loaned_item = self._loan_catalog.loan_item(item, self._client_id)

			if loaned_item is not None:
				successful_commits.append(item)
				loans.append(loaned_item)
			else:
				failed_commits.append(item)

		for item in successful_commits:
			self.delete_by_id(item.get_id(), item.record_type)

		return [loans, successful_commits, failed_commits]
