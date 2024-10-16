from typing import Any, Dict, List
import fitz
import pdfplumber
from data_extractor.data_extractor.extractor import Extractor

class PDFExtractor(Extractor):
    def __init__(self, loader):
        self.loader = loader
        self.file = None
        self.file_path = None

    def load(self, file_path):
        """Load the file using the appropriate loader based on file type."""
        self.file = self.loader.load_file(file_path)
        self.file_path = file_path 

    def extract_text(self):
        # Extract text from PDF
        text = ""
        for page in self.file.pages:
            text += page.extract_text()
        return text

    def extract_images(self):
        images = []
        # PDF image extraction
        pdf_document = fitz.open(self.file_path)
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            image_list = page.get_images(full=True)
            for img in image_list:
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                width, height = base_image["width"], base_image["height"]
                images.append({
                    "image_data": image_bytes,
                    "ext": image_ext,
                    "page": page_num + 1,
                    "dimensions": (width, height)
                })
        pdf_document.close()
        return images

    def extract_urls(self) -> List[Dict[str, Any]]:
        """Extract hyperlinks from a PDF file."""
        extracted_links = []
        for page_num, page in enumerate(self.file.pages, start=1):
            # Extract annotations from the page
            if '/Annots' in page:
                annotations = page['/Annots']
                for annot in annotations:
                    annot_obj = annot.get_object()  # Get the annotation object
                    # Check if the annotation object has the expected structure
                    if '/A' in annot_obj and '/URI' in annot_obj['/A']:
                        link = annot_obj['/A']['/URI']
                        extracted_links.append({                            
                            "linked_text": link,  # You can also extract the text if needed
                            "url": link,
                            "page_number": page_num
                        })
        return extracted_links

    def extract_tables(self):
        tables = []
        # Extract tables from PDF
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                # Extract tables from each page
                page_tables = page.extract_tables()
                for table in page_tables:
                    tables.append(table)  # Each table is a list of lists
        return tables