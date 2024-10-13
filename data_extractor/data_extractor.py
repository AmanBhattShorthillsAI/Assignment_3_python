import re
import fitz
import pdfplumber
from PyPDF2 import PdfReader

class DataExtractor:
    def __init__(self, loader):
        self.loader = loader
        self.file_path = loader.file_path

    def extract_text(self):
        """
        Extract text from the file.

        This method extracts text from the file based on the file type (PDF, DOCX, or PPTX).
        For PDFs, it uses the PyPDF2 library. For DOCX, it uses the python-docx library.
        For PPTX, it uses the python-pptx library.

        Args:
            None

        Returns:
            The extracted text as a string.

        Raises:
            ValueError: If the file type is not supported for text extraction.
        """
        if self.file_path.endswith('.pdf'):
            # Extract text from PDF
            reader = self.loader.load_file()
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text

        elif self.file_path.endswith('.docx'):
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

        elif self.file_path.endswith('.pptx'):
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

        else:
            raise ValueError("Unsupported file format for text extraction.")


    def extract_images(self):
        """
        Extract images from the given file.

        Images are extracted from PDF, DOCX, and PPTX files.

        Parameters
        ----------
        self : DataExtractor
            The data extractor object.

        Returns
        -------
        list
            A list of dictionaries containing information about the images.
            Each dictionary contains the image data, file extension, page number
            (for PDF and PPTX), and image dimensions (width, height).

        Notes
        -----
        The page number is 1-indexed, not 0-indexed.
        """
        images = []

        if self.file_path.endswith('.pdf'):
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

        elif self.file_path.endswith('.docx'):
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

        elif self.file_path.endswith('.pptx'):
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
        """
        Extract URLs from the given file.

        URLs are extracted from PDF, DOCX, and PPTX files.

        Parameters
        ----------
        self : DataExtractor
            The data extractor object.

        Returns
        -------
        list
            A list of URLs found in the file.

        Notes
        -----
        The URLs are extracted from text in the file using a regular expression.
        For PDFs, the URLs are extracted from text in the PDF. For DOCX and PPTX,
        the URLs are extracted from hyperlinks in the document.
        """
        urls = []

        if self.file_path.endswith('.pdf'):
            # Use PdfReader instead of PdfFileReader
            pdf_reader = PdfReader(self.file_path)
            for page_number in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_number]
                pdf_text = page.extract_text()  # Updated method to extract text
                # Use regex to find URLs
                regex = r"(https?://\S+)"
                url = re.findall(regex, pdf_text)
                urls += [x for x in url]  # Add found URLs to the list

        elif self.file_path.endswith('.docx'):
            # DOCX URL extraction using python-docx
            doc = self.loader.load_file()
            for paragraph in doc.paragraphs:
                for run in paragraph.runs:
                    # Check if the run has a hyperlink
                    hyperlink = run.element.xpath(".//w:hyperlink")
                    if hyperlink:
                        for link in hyperlink:
                            r_id = link.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
                            # Get the actual URL from the relationship
                            if r_id and r_id in doc.part.rels:
                                url = doc.part.rels[r_id].target_ref
                                urls.append(url)

        elif self.file_path.endswith('.pptx'):
            # PPTX URL extraction using python-pptx
            ppt = self.loader.load_file()
            for slide in ppt.slides:
                for shape in slide.shapes:
                    if shape.has_text_frame:
                        for paragraph in shape.text_frame.paragraphs:
                            for run in paragraph.runs:
                                # Extract the hyperlink, if present
                                hyperlink = run.hyperlink
                                if hyperlink and hyperlink.address:
                                    urls.append(hyperlink.address)
        return urls

        
    def extract_tables(self):
        """
        Extracts tables from the given file.

        Supported file formats are PDF, DOCX, and PPTX.

        For PDFs, uses pdfplumber to extract tables from each page. Each table is a list of lists.

        For DOCX, uses python-docx to extract tables. Each table is a list of lists.

        For PPTX, uses python-pptx to extract tables from shapes. Each table is a list of lists.

        Returns a list of tables. If no tables are found, an empty list is returned.

        Raises a ValueError if the file format is not supported.
        """
        tables = []

        if self.file_path.endswith('.pdf'):
            # Extract tables from PDF
            with pdfplumber.open(self.file_path) as pdf:
                for page in pdf.pages:
                    # Extract tables from each page
                    page_tables = page.extract_tables()
                    for table in page_tables:
                        tables.append(table)  # Each table is a list of lists
            return tables

        elif self.file_path.endswith('.docx'):
            # Extract tables from DOCX
            doc = self.loader.load_file()
            table_data = []
            for table in doc.tables:
                table_content = [[cell.text.strip() for cell in row.cells] for row in table.rows]
                table_data.append(table_content)
            return table_data

        elif self.file_path.endswith('.pptx'):
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

        else:
            raise ValueError("Unsupported file format for table extraction.")
