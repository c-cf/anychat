from abc import ABC, abstractmethod

class LLMInterface(ABC):
    @abstractmethod
    async def load_documents(self, directory: str):
        pass

    @abstractmethod
    async def generate(self, prompt: str):
        pass