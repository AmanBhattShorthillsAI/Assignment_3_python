import os
from PyPDF2 import PdfReader
from data_extractor.file_loaders.file_loader import FileLoader

class PDFLoader(FileLoader):
    def __init__(self, file_path):
        """
        Initialize a PDFLoader.

        :param file_path: The path to the PDF file to be loaded.
        """
        super().__init__(file_path)
        self.file = None

    def validate_file(self):
        """
        Validate if the file can be loaded.

        This method checks if the file exists and if it is a PDF file. If the
        file does not exist or is not a PDF file, an exception is raised.

        :raises ValueError: If the file can not be loaded.
        """
        if not os.path.exists(self.file_path):
            raise ValueError(f"File not found: {self.file_path}")
        if not self.file_path.lower().endswith(".pdf"):
            raise ValueError(f"Invalid file type: {self.file_path} is not a PDF file.")

    def load_file(self):
        """
        Load the PDF file.

        This method opens the file in binary mode and uses PyPDF2 to read the
        PDF file.

        :return: A PyPDF2.PdfReader object.
        :raises ValueError: If there is an error loading the PDF file.
        """
        try:
            self.file = open(self.file_path, "rb")
            return PdfReader(self.file)
        except Exception as e:
            raise ValueError(f"Error loading PDF file: {e}")

    def close_file(self):
        """
        Close the PDF file.

        This method closes the file after it has been loaded.

        :return: None
        """
        if self.file:
            self.file.close()