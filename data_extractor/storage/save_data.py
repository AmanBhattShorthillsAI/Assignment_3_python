import os
from data_extractor.storage.file_storage import FileStorage
from data_extractor.storage.sql_storage import SQLStorage
from dotenv import load_dotenv
load_dotenv()

class SaveData():
    def __init__(self, dataToBeSaved, file_path):
        self.file_path = file_path
        self.fileName = os.path.basename(file_path) 
        self.database_name = os.getenv("DATABASE_NAME")
        self.table_name_text = os.getenv("TABLE_NAME_TEXT")
        self.table_name_image = os.getenv("TABLE_NAME_IMAGE")
        self.table_name_url = os.getenv("TABLE_NAME_URL")
        self.table_name_data_table = os.getenv("TABLE_NAME_DATA_TABLE")
        
        # this will be used to store the extracted data and handle the errors
        self.extracted_text = dataToBeSaved.get("text", None)
        self.extracted_images = dataToBeSaved.get("images", None)
        self.extracted_urls = dataToBeSaved.get("urls", None)
        self.extracted_tables = dataToBeSaved.get("tables", None)
        
    def saveToLocal(self):
        # Create a folder for storing the extracted data
        base_name = os.path.splitext(os.path.basename(self.file_path))[0]
        output_dir = os.path.join("extracted_data", base_name)
        file_storage = FileStorage(output_dir)
        
        # Save the extracted text
        file_storage.store(self.extracted_text, os.path.basename(self.file_path), self.table_name_text)

        # Save the extracted images
        if self.extracted_images:
            file_storage.store(self.extracted_images, os.path.basename(self.file_path), self.table_name_image)

        # Save the extracted URLs (if any)
        if self.extracted_urls:
            file_storage.store(self.extracted_urls, os.path.basename(self.file_path), self.table_name_url)

        # Save the extracted tables (if any)
        if self.extracted_tables:
            file_storage.store(self.extracted_tables, os.path.basename(self.file_path), self.table_name_data_table)

        print(f"Extracted data saved to: {output_dir}")
        
    def saveToSQLDatabase(self):
        # Create an instance of SQLStorage
        sql_storage = SQLStorage(self.database_name)

        # Store the extracted text in the SQL database
        sql_storage.store(self.table_name_text, self.extracted_text, self.fileName)

        # Store the extracted images in the SQL database
        if self.extracted_images:
            sql_storage.store(self.table_name_image, self.extracted_images, self.fileName)

        # Store the extracted URLs in the SQL database
        if self.extracted_urls:
            sql_storage.store(self.table_name_url, self.extracted_urls, self.fileName)

        # Store the extracted tables in the SQL database
        if self.extracted_tables:
            for table in self.extracted_tables:
                sql_storage.store(self.table_name_data_table, table, self.fileName)

        print("Data stored in SQL database")
        sql_storage.close()