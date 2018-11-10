from app.controllers.controller import Controller
from app.classes.catalogs import UserCatalog
from app.classes.user import Admin, Client
from app.classes.user_container import User


class ClientController(Controller):

    def __init__(self, database):
        Controller.__init__(self, database)

        self._db_loaded = False

        self._client_catalog = UserCatalog(database)

    def load_database_into_memory(self):

        # Database cannot be loaded into RAM more than once
        if not (self._db_loaded):
            self._db_loaded = True

        # Add all objects form database into catalogs
        sql_query = """ SELECT * FROM client WHERE isAdmin = 0 """

        all_rows = self.db.execute_query(sql_query).fetchall()

        # Create an object for each row
        for row in all_rows:
            self._client_catalog.add(Client(row), False)

        # Uncomment these two lines to see all objects in all catalogs
        #for k, v in self._client_catalog.get_all().items():
        #    print(v)

    def get_all_logged_clients(self):

        return list(self._client_catalog.get_all().values())

    # function takes self and a string "username" to get the user from the client table.
    # returns list with client information or emptylist if client doesn't
    # exist in database
    def get_client_by_username(self, username):

        found_client = []

        clients = self._client_catalog.get_all()

        for id, clientObj in clients.items():

            if clientObj._username == username:
                found_client.append(clientObj)

        return found_client

    # function takes self and a string "email" to get the user from the client table.
    # returns list with client information or emptylist if client doesn't
    # exist in database
    def get_client_by_email(self, email):


        found_client = []

        clients = self._client_catalog.get_all()

        for id, clientObj in clients.items():

            if clientObj._email == email:
                found_client.append(clientObj)

        return found_client

    # function takes self and a string "username" & "password" to get the client from the client table.
    # if client exits, returns list with client information and updates value
    # in attribute isLogged to 1. Returns emptylist if client doesn't exist in
    # database
    def get_client_by_password(self, username, password):

        found_client = []

        clients = self._client_catalog.get_all()

        for id, clientObj in clients.items():

            if clientObj._username == username and clientObj._password == password:
                found_client.append(clientObj)

        return found_client



    # function takes self and username
    # updates value in attribute isLogged to 0.
    def logout_client(self, username):
        """
        self.db.execute_query_write(
            "UPDATE client SET isLogged = 0 WHERE username = ?", (username,))
        """

        client = self.get_client_by_username(username)

        # Mark client as logged out
        if len(client) == 1:
            client = client[0]
            client._is_logged = 0
            self._client_catalog.modify(client)

        print("Client has been logged out")
        return True

    # function takes self and several values to create a client
    # inserts a new client into the client table
    def create_client(self, firstName, lastName, physicalAddress, email, phoneNumber, username, password,
                      isLogged, lastLogged):

        attributesDict = {"firstName": firstName, "lastName": lastName, "physicalAddress": physicalAddress,
                          "email": email, "phoneNumber": phoneNumber, "username": username, "password": password,
                          "isAdmin": 0, "isLogged": isLogged, "lastLogged": lastLogged}

        self._client_catalog.add(Client(attributesDict), True)
