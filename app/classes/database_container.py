import sqlite3
import sys


class DatabaseContainer(object):
    """
    This class uses the Singleton pattern.
    """
    _instance = None

    @staticmethod
    def get_instance(path_to_database):
        """ Static access method. """
        if DatabaseContainer._instance is None:
            DatabaseContainer(path_to_database)
        return DatabaseContainer._instance

    def __init__(self, path_to_database):
        if DatabaseContainer._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DatabaseContainer._instance = self
            # Connect to database immediately
            self.connection = None
            self.dbPath = path_to_database

            try:
                # Make database useable in all threads
                self.connection = sqlite3.connect(
                    path_to_database, check_same_thread=False)

                # Make database accessible through index and keys
                self.connection.row_factory = sqlite3.Row

                print("Made connection!")
            except Error as e:
                print(e)
                sys.exit()

    def execute_query(self, sqlQuery, inputParameters=None):
        """
        This function executes a query and returns the cursor linked to the query
        The input parameter is optional
        """

        # Create new cursor
        cursor = self.connection.cursor()

        if inputParameters == None:
            cursor.execute(sqlQuery)
        else:
            cursor.execute(sqlQuery, inputParameters)

        return cursor

    def execute_query_write(self, sqlQuery, inputParameters=None):
        """
        This function executes a query, commits changes in the database and returns the cursor linked to the query
        The input parameter is optional
        """

        # Create new cursor
        cursor = self.connection.cursor()

        if inputParameters == None:
            cursor.execute(sqlQuery)
        else:
            cursor.execute(sqlQuery, inputParameters)

        self.connection.commit()

        return cursor

    def close_connection(self):
        try:
            self.connection.close()
        except Error as e:
            print(e)

    def print_path(self):
        print(self.dbPath)
