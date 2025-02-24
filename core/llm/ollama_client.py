from .base import LLMInterface
import httpx

class OllamaClient(LLMInterface):
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url
        self.model = model
        
    async def generate(self, prompt: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={"model": self.model, "prompt": prompt}
            )
            return response.json()["response"] 