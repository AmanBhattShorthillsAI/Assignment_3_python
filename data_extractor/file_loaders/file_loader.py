from abc import ABC, abstractmethod
from typing import Any

class FileLoader(ABC):
    # def __init__(self, file_path):
    #     """
    #     Initialize a FileLoader.

    #     :param file_path: The path to the file that should be loaded.
    #     """
    #     self.file_path = file_path
    #     self.validate_file(self.file_path)

    @abstractmethod
    def validate_file(self, file_path: str) -> bool:
        """Validate the file format."""
        pass

    @abstractmethod
    def load_file(self, file_path: str) -> Any:
        """Load and return the file object."""
        pass

    # @abstractmethod
    # def close_file(self):
    #     """
    #     Close the file.

    #     This method should be implemented by each subclass to close the file
    #     once it is no longer needed.

    #     :return: None
    #     """
    #     pass