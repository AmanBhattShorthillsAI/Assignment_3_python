from data_extractor.storage.storage import Storage

class SQLStorage(Storage):
    def __init__(self):
        """
        Initializes a SQLStorage instance.

        This constructor calls the super class's constructor to set up the connection to the database.
        """
        super().__init__()

    def store(self, table_name, data):
        # Sanitize the table_name variable
        """
        Stores data in a SQL database.

        :param table_name: The name of the table to store the data in.
        :param data: The data to be stored.
        """
        table_name = table_name.replace(" ", "_").replace("-", "_")

        # Create the table if it doesn't exist
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT
        )""")

        # Insert the data into the table
        self.cursor.execute(f"INSERT INTO {table_name} (data) VALUES (?)", (str(data),))

        # Commit the changes
        self.conn.commit()


    def close(self):
        """
        Closes the connection to the database.
        """
        self.conn.close()