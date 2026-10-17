from langchain_google_genai import ChatGoogleGenerativeAI

from config import settings



gemini_model = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", api_key=settings.settings.GOOGLE_API_KEY, max_tokens=100, temperature=0.2)