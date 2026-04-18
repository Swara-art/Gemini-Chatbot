from google import genai
from google.genai import types
from app.core.config import GEMINI_API_KEY, MODEL_NAME

class GeminiService:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.user_memory = {}
        self.search_tool = types.Tool(
            google_search=types.GoogleSearch()
        )

    def get_history(self, user_id: str):
        if user_id not in self.user_memory:
            self.user_memory[user_id] = []
        return self.user_memory[user_id]

    async def generate_response(self, user_id: str, prompt: str):
        try:
            # Retrieve or initialize history for the user
            history = self.get_history(user_id)
            
            # Start a chat session with the existing history and tools
            chat = self.client.chats.create(
                model=MODEL_NAME,
                config=types.GenerateContentConfig(
                    tools=[self.search_tool],
                    system_instruction="You are a helpful AI assistant with real-time search capabilities."
                ),
                history=history
            )
            
            # Send the user message
            response = chat.send_message(prompt)
            
            # Update history using the correct method for this SDK version
            self.user_memory[user_id] = chat.get_history()

            
            return response.text
        except Exception as e:
            if "429" in str(e):
                return "I'm sorry, but it seems I've hit my free usage limit (quota). Please try again in a minute."
            return f"An error occurred: {str(e)}"
