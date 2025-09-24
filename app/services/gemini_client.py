import os
import google.generativeai as genai
import logging

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "models/gemini-1.5-flash")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel(GEMINI_MODEL)
else:
    gemini_model = None

class GeminiClient:
    def __init__(self):
        self.model = gemini_model
        self.max_tokens = int(os.getenv("MAX_TOKENS", 1024))
        self.temperature = float(os.getenv("TEMPERATURE", 0.7))

    def generate_response(self, prompt: str) -> str:
        if not self.model:
            return "Gemini API key not configured."
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "max_output_tokens": self.max_tokens,
                    "temperature": self.temperature
                }
            )
            return response.text.strip()
        except Exception as e:
            logging.exception(f"Gemini API error: {e}")
            return "Sorry, I'm having trouble right now. Please try again later."
