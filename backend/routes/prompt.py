from chromadb import CloudClient
from groq import Groq
from fastapi import APIRouter, HTTPException 
from pydantic import BaseModel
import cohere
from conf import settings
from rank_bm25 import BM25Okapi
from utils.llm import query_groq
from utils.clean_query import clean_query
from utils.context_retrieval import query_chroma, query_bm25
from utils.context_processing import process_chunks

router = APIRouter()

# init clients
chroma_client = CloudClient(api_key=settings.CHROMA_API_KEY, database=settings.CHROMA_DATABASE, tenant=settings.CHROMA_TENANT)
groq_client = Groq()
cohere_client = cohere.Client(settings.CO_API_KEY)

# Data models
class PromptRequest(BaseModel):
    prompt: str

class PromptResponse(BaseModel):
    response: str

# API Endpoints
@router.post("/prompt", response_model=PromptResponse)
def prompt(req: PromptRequest):
    if not req.prompt or req.prompt.strip() == "":
        raise HTTPException(status_code=400, detail="Prompt is required")
    
    # Clean and optimize the query
    query = clean_query(groq_client, query=req.prompt)
    
    # Semantic search with ChromaDB
    semantic_chunks = query_chroma(chroma_client, query)

    # Keyword search with BM25
    bm25_chunks = query_bm25(BM25Okapi, groq_client, query)

    # Combine chunks
    all_chunks = list(semantic_chunks) + list(bm25_chunks)

    # Process chunks (deduplication and reranking)
    processed_chunks = process_chunks(cohere_client, query, all_chunks)

    # Use chunks to generate personalized response to prompt
    # optional: stream response on frontend
    ans = query_groq(groq_client, query, processed_chunks)

    if not ans or ans.strip() == "":
        raise HTTPException(status_code=404, detail="AI response not found")
    
    return PromptResponse(response=ans)
