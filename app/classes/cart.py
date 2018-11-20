class Cart:
	def __init__(self):
		self._items = set()

	def get_set(self):
		return self._items

	def add_to_cart(self, item):
		self._items.add(item)

	def delete_by_id(self, id):
		for item in self._items:
			if item.get_id() == id:
				self._items.discard(item)
				return "success"
			else:
				return "error"

	def make_loan(self):
		print("implementation required")