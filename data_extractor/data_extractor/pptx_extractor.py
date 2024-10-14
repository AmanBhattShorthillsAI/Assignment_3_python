import fitz
from data_extractor.extractor.extractor import Extractor

class PPTXExtractor(Extractor):
    def __init__(self, loader):
        super().__init__(loader)
        self.file_path = loader.file_path

    def extract_text(self):
        # Extract text from PPTX
        ppt = self.loader.load_file()
        text = ""

        # Extract text from shapes
        for slide in ppt.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text += shape.text + "\n"

                # Extract text from tables within shapes
                if shape.has_table:
                    for row in shape.table.rows:
                        row_text = "\t".join(cell.text.strip() for cell in row.cells)
                        text += row_text + "\n"

        return text

    def extract_images(self):
        images = []
        # PPTX image extraction
        ppt = self.loader.load_file()
        # Extract images
        for slide_num, slide in enumerate(ppt.slides):
            for shape in slide.shapes:
                if shape.shape_type == 13:  # Picture type
                    image_stream = shape.image.blob
                    image_ext = shape.image.ext
                    images.append({
                        "image_data": image_stream,
                        "ext": image_ext,
                        "page": slide_num + 1,
                    })
        return images

    def extract_urls(self):
        urls = []
        pdf_document = fitz.open(self.file)
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
        tables=[]
        # Extract tables from PPTX (typically tables are part of shapes)
        ppt = self.loader.load_file()
        for slide in ppt.slides:
            for shape in slide.shapes:
                if shape.has_table:  # Check if the shape contains a table
                    table_content = []
                    table = shape.table
                    for row in table.rows:
                        row_data = [cell.text_frame.text.strip() if cell.text_frame else '' for cell in row.cells]
                        table_content.append(row_data)
                    tables.append(table_content)
        return tables