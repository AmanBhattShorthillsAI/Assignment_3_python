from abc import ABC, abstractmethod

class FileLoader(ABC):
    def __init__(self, file_path):
        """
        Initialize a FileLoader.

        :param file_path: The path to the file that should be loaded.
        """
        self.file_path = file_path
        self.validate_file()

    @abstractmethod
    def validate_file(self):
        """
        Validate if the file can be loaded.

        This method should be implemented by each subclass to validate if the
        file can be loaded. If the file can not be loaded, an exception should
        be raised.

        :raises ValueError: If the file can not be loaded.
        """
        pass

    @abstractmethod
    def load_file(self):
        """
        Load the file.

        This method should be implemented by each subclass to load the file.

        :return: The loaded file.
        """
        pass

    @abstractmethod
    def close_file(self):
        """
        Close the file.

        This method should be implemented by each subclass to close the file
        once it is no longer needed.

        :return: None
        """
        pass