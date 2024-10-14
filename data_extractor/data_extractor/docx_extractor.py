import fitz
from data_extractor.extractor.extractor import Extractor

class DOCXExtractor(Extractor):
    def __init__(self, loader):
        super().__init__(loader)
        self.file_path = loader.file_path
        
    def extract_text(self):
        # Extract text from DOCX
            doc = self.loader.load_file()
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
        doc = self.loader.load_file()
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
    
    def extract_urls(self):
        urls = []
        pdf_document = fitz.open(self.file_path)
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            links = page.get_links()
            for link in links:
                if "uri" in link:
                    url = link["uri"]
                    rect = link["from"]
                    urls.append({
                        "url": url,
                        "page": page_num + 1,
                        "position": {
                            "x0": rect.x0,
                            "y0": rect.y0,
                            "x1": rect.x1,
                            "y1": rect.y1
                        }
                    })
        pdf_document.close()
        return urls
    
    def extract_tables(self):
        # Extract tables from DOCX
        doc = self.loader.load_file()
        table_data = []
        for table in doc.tables:
            table_content = [[cell.text.strip() for cell in row.cells] for row in table.rows]
            table_data.append(table_content)
        return table_data