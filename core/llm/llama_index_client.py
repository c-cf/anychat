from .base import LLMInterface
from llama_index import VectorStoreIndex, SimpleDirectoryReader

class LlamaIndexClient(LLMInterface):
    def __init__(self):
        self.index = None
        
    async def load_documents(self, directory: str):
        documents = SimpleDirectoryReader(directory).load_data()
        self.index = VectorStoreIndex.from_documents(documents)
        
    async def generate(self, prompt: str):
        if not self.index:
            raise ValueError("Documents not loaded")
        query_engine = self.index.as_query_engine()
        response = query_engine.query(prompt)
        return str(response) 