from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")
    CHROMA_TENANT: str | None = os.getenv("CHROMA_TENANT")
    CHROMA_DATABASE: str | None = os.getenv("CHROMA_DATABASE")
    CHROMA_API_KEY: str | None = os.getenv("CHROMA_API_KEY")
    CO_API_KEY: str | None = os.getenv("CO_API_KEY")

settings = Settings()