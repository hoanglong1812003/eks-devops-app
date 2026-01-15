import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    LLM_MODEL = "llama-3.1-8b-instant"
    LLM_TEMPERATURE = 0.1
    VECTORSTORE_PATH = "vectorstore"
    DATA_PATH = "data"
    CACHE_FOLDER = "/tmp/huggingface"
    
    # RAG settings
    SEARCH_TYPE = "mmr"
    SEARCH_K = 5
    FETCH_K = 10
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 100

settings = Settings()
