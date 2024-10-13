import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from data_extractor.file_loaders.pdf_loader import PDFLoader
from data_extractor.file_loaders.docx_loader import DOCXLoader
from data_extractor.file_loaders.ppt_loader import PPTLoader

class TestFileLoaders(unittest.TestCase):

    def test_pdf_loader(self):
        """
        Tests the PDFLoader's validate_file method with a valid PDF file.

        Asserts that the PDFLoader's validate_file method returns True for a valid PDF file.
        """
        self.file_path = "/home/shtlp_0071/Documents/assignment4/files/sample.pdf"
        loader = PDFLoader(self.file_path)
        self.assertTrue(loader.validate_file())

    def test_docx_loader(self):
        """
        Tests the DOCXLoader's validate_file method with a valid DOCX file.

        Asserts that the DOCXLoader's validate_file method returns True for a valid DOCX file.
        """
        self.file_path = "/home/shtlp_0071/Documents/assignment4/files/sample.docx"
        loader = DOCXLoader(self.file_path)
        self.assertTrue(loader.validate_file())

    def test_ppt_loader(self):
        """
        Tests the PPTLoader's validate_file method with a valid PPTX file.

        Asserts that the PPTLoader's validate_file method returns True for a valid PPTX file.
        """
        self.file_path = "/home/shtlp_0071/Documents/assignment4/files/sample.pptx"
        loader = PPTLoader(self.file_path)
        self.assertTrue(loader.validate_file())

    def test_pdf_loader_invalid_file(self):
        """
        Tests the PDFLoader's validate_file method with an invalid PDF file.

        Asserts that the PDFLoader's validate_file method returns False for a non-existent PDF file.
        """
        self.file_path = "/home/shtlp_0071/Documents/assignment4/files/non_existent_file.pdf"
        loader = PDFLoader(self.file_path)
        self.assertFalse(loader.validate_file())

    def test_docx_loader_invalid_file(self):
        """
        Tests the DOCXLoader's validate_file method with an invalid DOCX file.

        Asserts that the DOCXLoader's validate_file method returns False for a non-existent DOCX file.
        """
        self.file_path = "/home/shtlp_0071/Documents/assignment4/files/non_existent_file.docx"
        loader = DOCXLoader(self.file_path)
        self.assertFalse(loader.validate_file())

    def test_ppt_loader_invalid_file(self):
        """
        Tests the PPTLoader's validate_file method with an invalid PPTX file.

        Asserts that the PPTLoader's validate_file method returns False for a non-existent PPTX file.
        """
        self.file_path = "/home/shtlp_0071/Documents/assignment4/files/non_existent_file.pptx"
        loader = PPTLoader(self.file_path)
        self.assertFalse(loader.validate_file())

if __name__ == '__main__':
    unittest.main()