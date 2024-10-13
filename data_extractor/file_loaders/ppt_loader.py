import pptx
from data_extractor.file_loaders.file_loader import FileLoader

class PPTLoader(FileLoader):
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = None
    
    def validate_file(self):
        if not self.file_path.endswith('.pptx'):
            raise ValueError("Invalid file type. Expected a PPT file.")

    def load_file(self):
        return pptx.Presentation(self.file_path)
    
    def close_file(self):
        if self.file:
            self.file.close()