from typing import Any, Dict, List
import fitz
from data_extractor.data_extractor.extractor import Extractor

class DOCXExtractor(Extractor):
    def __init__(self, loader):
        self.loader = loader
        self.file = None
        self.file_path = None
        
    def load(self, file_path):
        """Load the file using the appropriate loader based on file type."""
        self.file = self.loader.load_file(file_path)
        self.file_path = file_path 
        
    def extract_text(self):
        # Extract text from DOCX
            doc = self.loader.load_file(self.file_path)
            text = ""

            # Extract text from paragraphs
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"

            # Extract text from tables
            for table in doc.tables:
                for row in table.rows:
                    row_text = "\t".join(cell.text.strip() for cell in row.cells)
                    text += row_text + "\n"

            return text
    
    def extract_images(self):
        images = []
        # DOCX image extraction
        doc = self.loader.load_file(self.file_path)
        for rel in doc.part.rels.values():
            if "image" in rel.target_ref:
                image_blob = rel.target_part.blob
                # Get the image extension
                image_ext = rel.target_part.content_type.split('/')[1]
                # Append the image information only if it is not None
                if image_blob is not None:
                    images.append({
                        "image_data": image_blob,
                        "ext": image_ext
                    })
        doc = None  # Explicitly close the document
        return images
    
    def extract_urls(self) -> List[Dict[str, Any]]:
        """Extract hyperlinks from a DOCX file."""
        extracted_links = []

        # Access the document's relationships to find hyperlinks
        for rel in self.file.part.rels.values():
            if "hyperlink" in rel.reltype:
                # Extract the hyperlink target
                hyperlink = rel.target_ref
                
                # Look for the text associated with this hyperlink
                linked_text = None
                page_number = None
                for para_index, para in enumerate(self.file.paragraphs, start=1):
                    for run in para.runs:
                        if hyperlink in run._element.xml:
                            linked_text = run.text
                            page_number = para_index  # Using the paragraph index as the page number
                            break
                    if linked_text:
                        break
                
                # Append the link, associated text, and page number to the extracted links
                extracted_links.append({
                    "linked_text": linked_text or "",  # Use an empty string if no text is found
                    "url": hyperlink,
                    "page_number": page_number
                })

        return extracted_links



    def extract_tables(self):
        # Extract tables from DOCX
        doc = self.loader.load_file(self.file_path)
        table_data = []
        for table in doc.tables:
            table_content = [[cell.text.strip() for cell in row.cells] for row in table.rows]
            table_data.append(table_content)
        return table_data