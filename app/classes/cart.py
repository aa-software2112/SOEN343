class Cart:
	def __init__(self):
		self._items = set()

	def get_set(self):
		return self._items

	def add_to_cart(self, item):
		self._items.add(item)

	def delete_by_id(self, id):

	def make_loan(self):	
