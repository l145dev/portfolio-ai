from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.prompt import router as prompt_router

app = FastAPI()

# Chatgpt: added CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://www.l145.be"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prompt_router)