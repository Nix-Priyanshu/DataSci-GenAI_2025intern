from google import genai
from backend.config import GEMINI_API_KEY, MODEL_ID
import logging

# --- INITIALIZATION ---
# Using the new Client
client = genai.Client(api_key=GEMINI_API_KEY)


# --- API CALL with---
def generate_response(system_prompt, history_context):
        try:
            logging.info("Sending request to Gemini API")
            
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=f"{system_prompt}\n\nConversation History:\n{history_context}"
            )
            reply = getattr(response, "text", None) or "I couldn't generate a response."
            logging.info("Gemini response generated successfully")
            return reply
        
        except Exception as e:
            # Log error (for developers)
            logging.error("Gemini API error: %s", str(e))
            # User-friendly fallback
            return  "⚠️ I'm having trouble right now. Please try again."
            
