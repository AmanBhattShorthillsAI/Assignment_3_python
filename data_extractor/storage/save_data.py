import os

from data_extractor.storage.file_storage import FileStorage


class SaveData():
    def __init__(self, dataToBeSaved, file_path):
        self.dataToBeSaved = dataToBeSaved
        self.file_path = file_path
        
    def saveToLocal(self):
        # Create a folder for storing the extracted data
        base_name = os.path.splitext(os.path.basename(self.file_path))[0]
        output_dir = os.path.join("extracted_data", base_name)
        file_storage = FileStorage(output_dir)

        # Save the extracted text
        file_storage.store(extracted_text, os.path.basename(file_path), table_name_text)

        # Save the extracted images
        image_data = None
        if images:
            image_data = file_storage.store(images, os.path.basename(file_path), table_name_image)

        # Save the extracted URLs (if any)
        if urls:
            file_storage.store(urls, os.path.basename(file_path), table_name_url)

        # Save the extracted tables (if any)
        if tables:
            file_storage.store(tables, os.path.basename(file_path), 'table')

        print(f"Extracted data saved to: {output_dir}")
        pass
    
    def saveToDatabase(self):
        pass