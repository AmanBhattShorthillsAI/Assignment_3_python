import os
from data_extractor.data_extractor.docx_extractor import DOCXExtractor
from data_extractor.data_extractor.pdf_extractor import PDFExtractor
from data_extractor.data_extractor.pptx_extractor import PPTXExtractor
from data_extractor.file_loaders.pdf_loader import PDFLoader
from data_extractor.file_loaders.docx_loader import DOCXLoader
from data_extractor.file_loaders.ppt_loader import PPTLoader
from data_extractor.storage.file_storage import FileStorage
from data_extractor.storage.sql_storage import SQLStorage
from dotenv import load_dotenv
load_dotenv()

def main():
    # Get configuration from environment variables
    file_path = input("Enter the file path: ")
    database_name = os.getenv("DATABASE_NAME")
    table_name_text = os.getenv("TABLE_NAME_TEXT")
    table_name_image = os.getenv("TABLE_NAME_IMAGE")
    table_name_url = os.getenv("TABLE_NAME_URL")
    table_name_data_table = os.getenv("TABLE_NAME_DATA_TABLE")

    if not file_path:
        raise ValueError("FILE_PATH is not set in the environment file.")

    # Determine the file type and use the appropriate loader
    if file_path.endswith(".pdf"):
        loader = PDFLoader()
        extractor = PDFExtractor(loader)
    elif file_path.endswith(".docx"):
        loader = DOCXLoader()
        extractor = DOCXExtractor(loader)
    elif file_path.endswith(".pptx") or file_path.endswith(".ppt"):
        loader = PPTLoader()
        extractor = PPTXExtractor(loader)
    else:
        raise ValueError("Unsupported file format. Use PDF, DOCX, or PPTX.")

    # Extract text from the file
    extractor.load(file_path)
    extracted_text = extractor.extract_text()

    # Extract images (if available)
    images = extractor.extract_images()

    # Extract URLs (if it's a PDF or DOCX)
    urls = extractor.extract_urls()

    # Extract tables (for PDFs or DOCX only)
    tables = extractor.extract_tables()

    # Create a folder for storing the extracted data
    base_name = os.path.splitext(os.path.basename(file_path))[0]
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
    
    # Create an instance of SQLStorage
    sql_storage = SQLStorage(database_name)

    # Store the extracted text in the SQL database
    sql_storage.store(table_name_text, extracted_text)

    # Store the extracted images in the SQL database
    if images:
        sql_storage.store(table_name_image, image_data)

    # Store the extracted URLs in the SQL database
    if urls:
        sql_storage.store(table_name_url, urls)

    # Store the extracted tables in the SQL database
    if tables:
        for table in tables:
            sql_storage.store(table_name_data_table, table)

    print("Data stored in SQL database")
    sql_storage.close()

if __name__ == "__main__":
    main()