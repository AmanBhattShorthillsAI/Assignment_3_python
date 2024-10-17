from data_extractor.data_extractor.docx_extractor import DOCXExtractor
from data_extractor.data_extractor.pdf_extractor import PDFExtractor
from data_extractor.data_extractor.pptx_extractor import PPTXExtractor
from data_extractor.file_loaders.docx_loader import DOCXLoader
from data_extractor.file_loaders.pdf_loader import PDFLoader
from data_extractor.file_loaders.ppt_loader import PPTLoader


class ExtractData():
    def __init__(self, file_path):
        self.file_path = file_path
        
    def checkForExtension(self, file_path):
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
        
        # return the appropriate extractor
        return extractor

    def extractData(self):
        # check for extension
        extractor = self.checkForExtension(self.file_path)

        # Extract texts
        extractor.load(self.file_path)
        
        #extract texts 
        extracted_text = extractor.extract_text()

        # Extract images (if available)
        images = extractor.extract_images()
        
        # Extract URLs
        urls = extractor.extract_urls()

        # Extract tables
        tables = extractor.extract_tables()
        
        # return a dictionary of items extracted
        return {
            "text": extracted_text,
            "images": images,
            "urls": urls,
            "tables": tables}