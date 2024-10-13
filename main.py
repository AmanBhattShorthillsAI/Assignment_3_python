import os
from data_extractor.file_loaders.pdf_loader import PDFLoader
from data_extractor.file_loaders.docx_loader import DOCXLoader
from data_extractor.file_loaders.ppt_loader import PPTLoader
from data_extractor.data_extractor import DataExtractor
from data_extractor.storage.file_storage import FileStorage
from data_extractor.storage.sql_storage import SQLStorage

def main():
    """
    Main function for extracting data from a file.

    This function takes a file path as an argument, determines the file type (PDF, DOCX, or PPTX),
    uses the appropriate loader to validate and load the file, creates an instance of DataExtractor
    to extract content, and then saves the extracted data to a folder and a SQL database.

    Parameters:
        file_path (str): Path to the file to be processed

    Returns:
        None
    """
    file_path = "/home/shtlp_0071/Documents/assignment4/files/sample.pdf"  # Change this to the file you want to process

    # Determine the file type and use the appropriate loader
    if file_path.endswith(".pdf"):
        loader = PDFLoader(file_path)
    elif file_path.endswith(".docx"):
        loader = DOCXLoader(file_path)
    elif file_path.endswith(".pptx"):
        loader = PPTLoader(file_path)
    else:
        raise ValueError("Unsupported file format. Use PDF, DOCX, or PPTX.")

    # Validate the file (ensures it's the correct type)
    loader.validate_file()

    # Load the file using the appropriate loader
    loader.load_file()

    # Create an instance of DataExtractor for extracting content
    extractor = DataExtractor(loader)

    # Extract text from the file
    extracted_text = extractor.extract_text()

    # Extract images (if available)
    images = extractor.extract_images()

    # Extract URLs (if it's a PDF or DOCX)
    urls = extractor.extract_urls() if file_path.endswith(('.pdf', '.docx')) else None
    print(urls)

    # Extract tables (for PDFs or DOCX only)
    tables = extractor.extract_tables() if file_path.endswith(('.pdf', '.docx')) else None

    # Close the file (if applicable)
    if hasattr(loader, 'close_file'):
        loader.close_file()

    # Create a folder for storing the extracted data
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_dir = os.path.join("extracted_data", base_name)
    file_storage = FileStorage(output_dir)

    # Save the extracted text
    file_storage.save(extracted_text, os.path.basename(file_path), 'text')

    # Save the extracted images
    if images:
        file_storage.save(images, os.path.basename(file_path), 'image')

    # Save the extracted URLs (if any)
    if urls:
        file_storage.save(urls, os.path.basename(file_path), 'url')

    # Save the extracted tables (if any)
    if tables:
        file_storage.save(tables, os.path.basename(file_path), 'table')

    print(f"Extracted data saved to: {output_dir}")
    
    # Create an instance of SQLStorage
    sql_storage = SQLStorage()

    # Store the extracted text in the SQL database
    sql_storage.store("text", extracted_text)

    # Store the extracted images in the SQL database
    if images:
        sql_storage.store("image", images)

    # Store the extracted URLs in the SQL database
    if urls:
        sql_storage.store("url", urls)

    # # Store the extracted tables in the SQL database
    # if tables:
    #     for table in tables:
    #         sql_storage.store("table", table)

    print("Data stored in SQL database")
    sql_storage.close()
    loader.close_file()

if __name__ == "__main__":
    main()
