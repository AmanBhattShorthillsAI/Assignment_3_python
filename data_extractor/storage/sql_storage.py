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

        if(table_name == 'image'):
            self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {escaped_table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            page_number INT,
            data TEXT
            )""")
        else:
            self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {escaped_table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                data TEXT
            )""")

        # Insert the filename and data into the table
        if(table_name == 'image'):
            # print(data)
            for i in range(len(data)):
                self.cursor.execute(f"INSERT INTO {escaped_table_name} (filename, page_number, data) VALUES (?, ?, ?)", (filename, data[i]['page'], str(data[i]['image_data'])))
            # self.cursor.execute(f"INSERT INTO {escaped_table_name} (filename, page_number, data) VALUES (?, ?, ?)", (filename, data['page_number'], str(data['data'])))
        else:
            self.cursor.execute(f"INSERT INTO {escaped_table_name} (filename, data) VALUES (?, ?)", (filename, str(data)))

        # Commit the changes
        self.conn.commit()

    def close(self):
        self.conn.close()