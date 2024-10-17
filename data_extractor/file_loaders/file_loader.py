from abc import ABC, abstractmethod
from typing import Any

class FileLoader(ABC):
    @abstractmethod
    def validate_file(self, file_path: str) -> bool:
        """Validate the file format."""
        pass

    @abstractmethod
    def load_file(self, file_path: str) -> Any:
        """Load and return the file object."""
        pass