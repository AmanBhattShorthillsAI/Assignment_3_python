import sqlite3
from abc import ABC, abstractmethod

class Storage(ABC):
    def __init__(self):
        self.conn = sqlite3.connect('assignment4.db')
        self.cursor = self.conn.cursor()

    @abstractmethod
    def store(self):
        """Store the extracted data."""
        pass
    
    @abstractmethod
    def close(self):
        pass