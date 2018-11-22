class Cart:
	def __init__(self):
		self._items = set()

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

	def make_loan(self):
		print("implementation required")