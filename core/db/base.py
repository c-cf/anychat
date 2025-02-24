from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass

    @abstractmethod
    async def execute(self, query: str, params: dict):
        pass 