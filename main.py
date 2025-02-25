from fastapi import FastAPI, Lifespan
from dotenv import load_dotenv
from core.db.sqlite_database import SQLiteDatabase
import os

# Load environment variables
load_dotenv()

app = FastAPI(lifespan=Lifespan())

@app.lifespan
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()


# Initialize SQLite database
db = SQLiteDatabase("./app.db")

class Config:
    DB_TYPE = os.getenv("DB_TYPE", "sqlite")  # Default to SQLite
    DB_CONNECTION = os.getenv("DB_CONNECTION", "sqlite:///./app.db")  # SQLite connection string
    VECTOR_DB_TYPE = os.getenv("VECTOR_DB_TYPE", "qdrant")  # Default to Qdrant
    VECTOR_DB_URL = os.getenv("VECTOR_DB_URL", "http://localhost:6333")  # Qdrant URL
    LLM_TYPE = os.getenv("LLM_TYPE", "ollama")  # Default to Ollama
    LLM_MODEL = os.getenv("LLM_MODEL", "llama2")  # Default model
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
