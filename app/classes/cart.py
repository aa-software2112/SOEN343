class Cart:
    def __init__(self):
        self._items = set()

    def get_set(self):
        return self._items

    def add_to_cart(self, item):
        print(item)

        self._items.add(item)

    def length_of_cart(self):
        return self._items.__len__()



