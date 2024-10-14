import os
from PyPDF2 import PdfReader
from data_extractor.file_loaders.file_loader import FileLoader

class PDFLoader(FileLoader):
    # def __init__(self, file_path):
    #     """
    #     Initialize a PDFLoader.

    #     :param file_path: The path to the PDF file to be loaded.
    #     """
    #     super().__init__(file_path)
    #     self.file = None

    def validate_file(self, file_path: str) -> bool:
        return file_path.lower().endswith('.pdf')

    def load_file(self, file_path: str) -> PdfReader:
        if not self.validate_file(file_path):
            raise ValueError("Invalid PDF file.")
        return PdfReader(file_path)

    # def close_file(self):
    #     """
    #     Close the PDF file.

    #     This method closes the file after it has been loaded.

    #     :return: None
    #     """
    #     if self.file:
    #         self.file.close()