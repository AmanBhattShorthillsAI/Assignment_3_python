import pptx
from data_extractor.file_loaders.file_loader import FileLoader

class PPTLoader(FileLoader):
    # def __init__(self, file_path):
    #     self.file_path = file_path
    #     self.file = None
    
    def validate_file(self, file_path: str) -> bool:
        return file_path.lower().endswith('.pptx') or file_path.lower().endswith('.ppt')

    def load_file(self, file_path: str) -> pptx.Presentation:
        if not self.validate_file(file_path):
            raise ValueError("Invalid PPT file.")
        
        try:
            # Attempt to load the PPTX file
            return pptx.Presentation(file_path)
        except Exception:
            # Catch any exception related to loading the file and raise the expected error
            raise ValueError("Invalid PPT file.")


    
    # def close_file(self):
    #     if self.file:
    #         self.file.close()