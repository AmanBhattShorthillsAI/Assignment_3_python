from typing import Any, Dict, List
from data_extractor.data_extractor.extractor import Extractor

class PPTXExtractor(Extractor):
    def __init__(self, loader):
        self.loader = loader
        self.file = None
        self.file_path = None
        
    def load(self, file_path):
        """Load the file using the appropriate loader based on file type."""
        self.file = self.loader.load_file(file_path)
        self.file_path = file_path 

    def extract_text(self):
        # Extract text from PPTX
        ppt = self.loader.load_file(self.file_path)
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
        ppt = self.loader.load_file(self.file_path)
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

    def extract_urls(self) -> List[Dict[str, Any]]:
        """Extract hyperlinks from a PPTX file."""
        extracted_links = []
        # Loop through each slide in the presentation
        for slide_num, slide in enumerate(self.file.slides, start=1):
            # Loop through each shape in the slide
            for shape in slide.shapes:
                # Check if the shape has a text frame and it is not None
                if hasattr(shape, "text_frame") and shape.text_frame is not None:
                    # Loop through each paragraph in the text frame
                    for paragraph in shape.text_frame.paragraphs:
                        # Loop through each run in the paragraph
                        for run in paragraph.runs:
                            # Check if the run has a hyperlink and get the link address
                            if run.hyperlink and run.hyperlink.address:
                                extracted_links.append({
                                    "linked_text": run.text,  # Get the text of the hyperlink
                                    "url": run.hyperlink.address,  # Get the hyperlink address
                                    "page_number": slide_num  # Get the slide number
                                })
        return extracted_links

    def extract_tables(self):
        tables=[]
        # Extract tables from PPTX (typically tables are part of shapes)
        ppt = self.loader.load_file(self.file_path)
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