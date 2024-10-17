from data_extractor.storage.storage import Storage

class SQLStorage(Storage):
    def __init__(self, database):
        super().__init__(database)

    def store(self, table_name, data, filename):
        """
        Stores data and filename in a SQL database.

        :param table_name: The name of the table to store the data in.
        :param filename: The name of the file the data was extracted from.
        :param data: The data to be stored.
        """
        self.table_name = table_name.replace(" ", "_").replace("-", "_")

        # Create the table if it doesn't exist, with an additional 'filename' column
        escaped_table_name = f'"{self.table_name}"'

        # Use the same table creation logic for both 'image' and other table types
        if table_name == 'image':
            self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {escaped_table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                page_number INT,
                data TEXT
            )""")
            # Insert data for the 'image' table
            for entry in data:
                self.cursor.execute(
                    f"INSERT INTO {escaped_table_name} (filename, page_number, data) VALUES (?, ?, ?)",
                    (filename, entry['page'], str(entry['image_data']))
                )
        else:
            # Create a table for text or other data types
            self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {escaped_table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                data TEXT
            )""")
            # Insert data for the non-image table
            self.cursor.execute(
                f"INSERT INTO {escaped_table_name} (filename, data) VALUES (?, ?)",
                (filename, str(data))
            )

        # Commit the changes to the database
        self.conn.commit()

    def close(self):
        self.conn.close()