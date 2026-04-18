from fastapi import FastAPI
from app.routes.chat_routes import router as chat_router

app = FastAPI(title="Gemini Chatbot", description="A chatbot powered by Gemini API", version="1.0.0")

app.include_router(chat_router)

@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"message": "Welcome to the Gemini Chatbot API!"}


