from chromadb import CloudClient
from groq import Groq
from fastapi import APIRouter, HTTPException 
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# Initialize clients
chroma = CloudClient(api_key=os.environ["CHROMA_API_KEY"], database=os.environ["CHROMA_DATABASE"], tenant=os.environ["CHROMA_TENANT"])
groq = Groq()

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
    
    # Semantic search with ChromaDB
    results = query_chroma(req.prompt)

    # Use results to generate personalized response to prompt
    # TODO: stream response on frontend
    ans = query_groq(req.prompt, results)

    if not ans or ans.strip() == "":
        raise HTTPException(status_code=404, detail="AI response not found")
    
    return PromptResponse(response=ans)

# Helper functions
def query_chroma(query: str):
    collection = chroma.get_or_create_collection("aryan_portfolio")
    results = collection.query(query_texts=[query], n_results=5)
    return results

def query_groq(prompt: str, results):
    response = groq.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """
                    You will use the following writing style for all responses:
                    - Direct, confident, and concise communication
                    - Professional yet conversational tone
                    - Clear structure with logical flow between ideas
                    - Emphasis on ownership and impact ("I took full ownership", "I built")
                    - Explicit alignment of skills/interests with the context
                    - Practical focus on value creation and application
                    - Active voice and strong action verbs
                    - Connecting personal experiences to broader relevance
                    - Concise paragraphs that get straight to the point
                    - Natural transitions between technical and personal aspects
                    
                    Example (Not to be used literally): As for my professional experience, it was mostly frontend based, where I 
                        took full ownership over a web-based tool used by various departments 
                        within the company. Since it was a specialized tool, communication was 
                        key to designing it in a way which is ideal for the use case. I built out the 
                        design and made tests to ensure the web application works as expected. 
                        This development cycle is not only related to the web, and can be carried 
                        over to any stack.

                    Important: If the information is not available in the context, respond with "I could not find the information you requested. Please ask questions related to my skills, projects, experience and other relevant topics. To ensure you get concise answers, make sure your prompts are concise (ideally 1 sentence of 1-10 words per prompt), they do not have to be perfect english sentences."
                """
            },
            {
                "role": "user",
                "content": prompt + "\n\nUse the following context from Aryan's portfolio to answer the question:\n" + str(results),
            }
        ],
        model="openai/gpt-oss-20b",
        stream=False,
    )

    return response.choices[0].message.content
    
    # If streaming were enabled, handle the stream here
    # for chunk in response:
    #     if chunk.choices[0].delta.content is not None:
    #         print(chunk.choices[0].delta.content, end="")