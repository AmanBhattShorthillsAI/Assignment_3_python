from abc import ABC, abstractmethod

class Extractor(ABC):
    @abstractmethod
    def load(self, file_path):
        pass

    @abstractmethod
    def extract_text(self):
        pass
    
    @abstractmethod
    def extract_images(self):
        pass
    
    @abstractmethod
    def extract_urls(self):
        pass
    
    @abstractmethod
    def extract_tables(self):
        pass