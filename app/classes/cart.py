import app.classes.catalogs

class Cart:
    def __init__(self, client_id):
        self._items = set()
        self._client_id = client_id
        self._loan_catalog = app.classes.catalogs.LoanCatalog.get_instance()

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
        """
        successful_commits = []
        loans = []
        failed_commits = []
        items_to_delete = []

        for item in self._items:
            loaned_item = self._loan_catalog.loan_item(item, self._client_id)

            if loaned_item is not None:
                successful_commits.append(item)
                loans.append(loaned_item)
                items_to_delete.append(item)
            else:
                failed_commits.append(item)

        for item in items_to_delete:
            self.delete_by_id(item.get_id(), item.record_type)

        return [loans, successful_commits, failed_commits]
