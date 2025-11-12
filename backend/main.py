from fastapi import FastAPI
from routes.prompt import router as prompt_router

app = FastAPI()

app.include_router(prompt_router)